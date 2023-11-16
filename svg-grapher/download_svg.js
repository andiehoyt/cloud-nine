// Import the generateSVG function from graphplot..js
const generateSVG = require('./graphplot.js');

// Get the SVG content using the generateSVG function
const svgContent = generateSVG();

// Get a reference to the download button
const downloadButton = document.getElementById('downloadButton');

// Add a click event listener to trigger the download
downloadButton.addEventListener('click', () => {
    // Code to create and trigger the download
});

// Add a click event listener to trigger the download
downloadButton.addEventListener('click', () => {
    // Get the SVG content you want to download (replace with your actual SVG content)
    const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="50" cy="50" r="40" /></svg>`;

    // Create a Blob from the SVG content
    const blob = new Blob([svgContent], { type: 'image/svg+xml' });

    // Create a temporary URL for the Blob
    const url = URL.createObjectURL(blob);

    // Create an <a> element for downloading
    const a = document.createElement('a');
    a.href = url;
    a.download = 'graph.svg'; // Specify the filename for the download

    // Trigger the click event on the <a> element to start the download
    a.click();

    // Release the URL object to free up resources
    URL.revokeObjectURL(url);
});