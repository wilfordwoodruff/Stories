library(shiny)
library(dplyr)

shinyApp(
  ui = 
    fluidPage(
      # Display the row for the button clicked
      verbatimTextOutput("details"),
      fluidRow(
        column(width = 3,
               selectInput(inputId ="data_source",
                           label = "Select a data set",
                           choices = c("mtcars", "iris"))),
        column(width = 9,
               uiOutput("show_table"))
      )
    ),
  
  server = 
    shinyServer(function(input, output, session){
      
      # Store the details of the clicked row
      Data <- reactiveValues(
        Info = NULL
      )
      
      # One Observer to Rule Them All (evil cackle)
      # Update the Data$Info value.
      observe({
        # Identify all of the buttons in the table.
        # Note that I assumed the same prefix on all buttons, and 
        # they only differ on the number following the underscore
        # This must happen in an observed since the number of rows 
        # in the table is not fixed.
        input_btn <- paste0("btn_", seq_len(nrow(display_table())))
        lapply(input_btn,
               function(x){
                 observeEvent(
                   input[[x]],
                   {
                     i <- as.numeric(sub("btn_", "", x))
                     Data$Info <- display_table()[i, -length(display_table())]
                   }
                 )
               })
      })
      
      # Generate the table of data.  
      display_table <- 
        reactive({
          tbl <- 
            get(input$data_source) %>% 
            # Add the row names as a column (not always useful)
            cbind(row_id = rownames(.),
                  .) %>% 
            # Add the action buttons as the last column
            mutate(button = vapply(row_number(),
                                   function(i){
                                     actionButton(inputId = paste0("btn_", i),
                                                  label = "View Details") %>% 
                                       as.character()
                                   },
                                   character(1)))
        })
      
      # Render the table with the action buttons
      output$show_table <- 
        renderUI({
          display_table() %>% 
            select(row_id, button) %>% 
            knitr::kable(format = "html",
                         # very important to use escape = FALSE
                         escape = FALSE) %>% 
            HTML()
        })
      
      # Print the details to the screen.
      output$details <- 
        renderPrint({
          req(Data$Info)
          Data$Info
        })
    })
  
)