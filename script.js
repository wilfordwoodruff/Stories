function pushToGitHub() {
    // Define the repository details
    const owner = 'wilfordwoodruff';
    const repo = 'Public_Stories';
    const filePath = 'society/user_query.csv'; // The desired path and name of the CSV file in the repository
  
    // Define the content of the CSV file
    const csvContent = searched;

  
    // Set up the GitHub API endpoint
    const apiUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${filePath}`;
  
    // Create the file using the GitHub API
    fetch(apiUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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' // Replace with your personal access token
      },
      body: JSON.stringify({
        message: 'Add CSV file',
        content: btoa(csvContent) // Encode the CSV content as base64
      })
    })
    .then(response => {
      if (response.ok) {
        alert('CSV file pushed to GitHub successfully!');
      } else {
        alert('Failed to push CSV file to GitHub.');
      }
    })
    .catch(error => {
      alert('An error occurred while pushing the CSV file to GitHub.');
      console.error(error);
    });
  }

// Attach event handler to the button's click event
const myButton = document.getElementById('pushtoGithub()');
myButton.addEventListener('click', function() {
  // Pass the variable to the handleClick function
  const myVariable = 'Hello, world!';
  handleClick(myVariable);
});