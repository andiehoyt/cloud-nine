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
    let topicCounter = 0;

    data.forEach(row => {
        if (row.Strand !== currentStrand) {
            currentStrand = row.Strand;
            const strandHeader = document.createElement('h2');
            strandHeader.className = 'strand-header collapsible';
            strandHeader.textContent = currentStrand;
            const strandContent = document.createElement('div');
            strandContent.className = 'content';

            strandHeader.addEventListener('click', function() {
                strandContent.style.display = strandContent.style.display === 'none' ? '' : 'none';
            });

            gridContainer.appendChild(strandHeader);
            gridContainer.appendChild(strandContent);
        }

        if (row.topic_title !== currentTopic) {
            currentTopic = row.topic_title;
            topicCounter++;
            topicDiv = document.createElement('div');
            topicDiv.className = 'topic-container content';
            const topicHeader = document.createElement('h3');
            topicHeader.className = 'topic-subheader collapsible';
            topicHeader.textContent = currentTopic;

            list = document.createElement('ul');
            list.className = 'subtopic-list';
            list.setAttribute('data-topic', topicCounter);

            topicHeader.addEventListener('click', function() {
                const targetList = document.querySelector(`[data-topic="${topicCounter}"]`);
                targetList.style.display = targetList.style.display === 'none' ? '' : 'none';
            });

            topicDiv.appendChild(topicHeader);
            topicDiv.appendChild(list);
            strandContent.appendChild(topicDiv);
        }

        const listItem = document.createElement('li');
        listItem.className = 'subtopic-item';
        listItem.textContent = row.subtopic_title;
        list.appendChild(listItem);
    });
}
