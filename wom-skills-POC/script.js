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
    let topicDiv, list, strandContent;

    data.forEach(row => {
        // Check if the strand has changed
        if (row.Strand !== currentStrand) {
            currentStrand = row.Strand;
            const strandHeader = document.createElement('h2');
            strandHeader.className = 'strand-header collapsible';
            strandHeader.textContent = currentStrand;

            strandContent = document.createElement('div');
            strandContent.className = 'content'; 

            strandHeader.addEventListener('click', function() {
                this.classList.toggle("active");
                strandContent.style.display = strandContent.style.display === 'none' ? '' : 'none';
            });

            gridContainer.appendChild(strandHeader);
            gridContainer.appendChild(strandContent);
        }

        // Check if the topic has changed
        if (row.topic_title !== currentTopic) {
            currentTopic = row.topic_title;
            topicDiv = document.createElement('div');
            topicDiv.className = 'topic-container content';

            const topicHeader = document.createElement('h3');
            topicHeader.className = 'topic-subheader collapsible';
            topicHeader.textContent = currentTopic;

            list = document.createElement('ul');
            list.className = 'subtopic-list';

            topicHeader.addEventListener('click', function() {
                this.classList.toggle("active");
                list.style.display = list.style.display === 'none' ? '' : 'none';
            });

            topicDiv.appendChild(topicHeader);
            topicDiv.appendChild(list);
            strandContent.appendChild(topicDiv);
        }

        // Add subtopic as a list item
        const listItem = document.createElement('li');
        listItem.className = 'subtopic-item';
        listItem.textContent = row.subtopic_title;
        list.appendChild(listItem);
    });
}
