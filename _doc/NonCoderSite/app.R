#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(googlesheets4)
library(googledrive)
library(tidyverse)
library(DT)


writings <- read_csv('https://raw.githubusercontent.com/wilfordwoodruff/Public_Stories/main/code/Stories/maps/Sample%20Subset.csv')

drive_id <- drive_find('User Stories')
#tell terminal to answer "2"
stories <- drive_get(drive_id$id) %>%
  read_sheet()

# Define UI for application that draws a histogram
ui <- fluidPage(
  theme = bslib::bs_theme(bootswatch = "united"),
    # Application title
    titlePanel("Explore President Woodruff's Diaries"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            selectInput(inputId='chosen_preset',
                      label='See What Others have Found!',
                      choices=stories$Name),
            br(),
            dateRangeInput(inputId = "startEndDate",
                           label="Writing Period",
                           start=min(writings$`First Date`),
                           end=max(writings$`First Date`),
                           separator='Journals between',
                           min=min(writings$`First Date`),
                           max=max(writings$`First Date`)
                           ),
            checkboxGroupInput(inputId = 'journal_type',
                               label = 'Types of Writings',
                               choices = unique(writings$`Document Type`),
                               selected = unique(writings$`Document Type`)
              
            ),
            textInput(inputId='word_search',
                      label='Search for a Word',
                      value= "Utah"),
            br(),
            textInput(inputId='submit_name',
                      label='Name Your Discovery!'),
            textAreaInput(inputId='submit_description',
                      label='Describe What You Found',
                      width='400px',height='100px'),
            actionButton(inputId="saveStory",
                         label="Save Your Story")
        ),
        

        # Show a plot of the generated distribution
        mainPanel(
          tabsetPanel(
            tabPanel("See Dataset",
             tableOutput("fiverows")#,plotOutput("distplot")
            ),
            tabPanel("See Graphs",
                    plotOutput("all_graphs")
                    
            )
           )
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

  
  user_filters <- reactiveValues()
  user_filters$submit <- 0
  
  observe({
    if(input$chosen_preset!='Default') {
      selected <- filter(stories,Name==input$chosen_preset)
      user_filters$startdate=selected$StartDate[1]
      user_filters$enddate =selected$EndDate[1]
      user_filters$wordsearch = selected$Words[1]
      #input$ducks <- input$ducks-1
    }
    else {
      user_filters$startdate=input$startenddate[1]
      user_filters$enddate =input$startenddate[2]
      user_filters$wordsearch = input$word_search
    }
    if(input$saveStory > user_filters$submit) {
      current_submission <- c(input$submit_name,
                              ymd(input$startenddate[1]), #Start Day
                              ymd(input$startenddate[2]), #End Day
                              input$word_search,
                              input$journal_type,
                              NA,
                              input$submit_description)
      write_sheet(data=rbind(read_sheet(drive_get(drive_id$id)),
                             current_submission),
                  ss=drive_id$id,sheet='Main')
    }
  })
  output$fiverows <- renderTable({
    writings %>%
      mutate(`Word Count`=str_count(`Text Only Transcript`,user_filters$wordsearch)) %>%
      select(`Document Type`,`Text Only Transcript`,Places,Dates,`Word Count`) %>%
      filter(`Word Count` > 0 & `Document Type` %in% input$journal_type) %>%
      #add date filter
      head()}
    
  )
  #Plots--------------------
  output$sentiment_graph <- renderGraph({
    #ggplot stuff here, 
  })
  output$location_graph <- renderGraph({
    
  })
  output$frequency_graph <- renderGraph({
    
  })
  
}

"
Main pieces to filter by:
user_filters$startdate
            $enddate
            $word_search
            $journal_type
"


"
output$distPlot <- renderPlot({
  # generate bins based on input$bins from ui.R
  x    <- faithful[, 2]
  bins <- seq(min(x), max(x), length.out = input$bins + 1)
  
  # draw the histogram with the specified number of bins
  hist(x, breaks = bins, col = 'darkgray', border = 'white',
       xlab = 'Waiting time to next eruption (in mins)',
       main = 'Histogram of waiting times')
})
"
# Run the application 
shinyApp(ui = ui, server = server)
