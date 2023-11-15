document.addEventListener('DOMContentLoaded', function() {
    fetch('WOM.csv')
        .then(response => response.text())
        .then(csvText => Papa.parse(csvText, {
            header: true,
            complete: displayGrid
        }));
});

function displayGrid(result) {
    const data = result.data;
    const gridContainer = document.getElementById('grid-container');
    let currentStrand = '';
    let currentTopic = '';
    let topicDiv, list;

    data.forEach(row => {
        // Check if the strand has changed
        if (row.Strand !== currentStrand) {
            currentStrand = row.Strand;
            const strandHeader = document.createElement('h2');
            strandHeader.className = 'strand-header';
            strandHeader.textContent = currentStrand;
            gridContainer.appendChild(strandHeader);
        }

        // Check if the topic has changed
        if (row.topic_title !== currentTopic) {
            currentTopic = row.topic_title;
            topicDiv = document.createElement('div');
            const topicHeader = document.createElement('h3');
            topicHeader.className = 'topic-subheader';
            topicHeader.textContent = currentTopic;
            topicDiv.appendChild(topicHeader);

            // Create a new list for the subtopics
            list = document.createElement('ul');
            topicDiv.appendChild(list);
            gridContainer.appendChild(topicDiv);
        }

        // Add subtopic as a list item
        const listItem = document.createElement('li');
        listItem.className = 'subtopic-item';
        listItem.textContent = row.subtopic_title;
        list.appendChild(listItem);
    });
}
