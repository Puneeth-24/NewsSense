function loadImageAndData() {
    const imgElement = document.getElementById('generatedImage');
    const infoElement = document.getElementById('infoDisplay');
  
    const apiUrl = 'http://127.0.0.1:5000/generate-image-and-data';
  
    fetch(apiUrl)
      .then(response => {
          return response.json();
      })
      .then(data => {
        if (data.success) {
          if (data.dictionaryData && infoElement) {
             console.log("Dictionary Data:", data.dictionaryData);
  
             const name = data.dictionaryData.Name;
             const ticker = data.dictionaryData.ticker;
             const percent = data.dictionaryData.percent;
             const status = data.dictionaryData.status;

             // Format the output based on data availability
             let output = '';
             if (name !== "N/A") {
               output += `Company: ${name}\n`;
             }
             if (ticker !== "N/A") {
               output += `Ticker: ${ticker}\n`;
             }
             if (percent !== "N/A") {
               output += `Daily Change: ${percent}%\n`;
             }
             output += `Status: ${status.replace('_', ' ')}`;

             infoElement.textContent = output;
          } else {
             console.warn("Dictionary data missing or display element not found.");
          }
  
          if (data.imageData) {
             imgElement.src = 'data:image/png;base64,' + data.imageData;
          } else {
             console.error("Image data missing in response.");
          }
        } else {
          console.error("API call failed:", data.error);
        }
      })
      .catch(error => {
        console.error('Error fetching image and data:', error);
      });
}

loadImageAndData(); 