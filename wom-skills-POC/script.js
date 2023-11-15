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
    let strandCounter = 0;
    let topicCounter = 0;

    data.forEach(row => {
        if (row.Strand !== currentStrand) {
            currentStrand = row.Strand;
            strandCounter++;
            topicCounter = 0; // Reset topic counter for each new strand

            const strandHeader = document.createElement('h2');
            strandHeader.className = 'strand-header collapsible';
            strandHeader.textContent = currentStrand;
            strandHeader.setAttribute('data-strand', strandCounter);

            const strandContent = document.createElement('div');
            strandContent.className = 'content';
            strandContent.setAttribute('data-strand-content', strandCounter);

            strandHeader.addEventListener('click', function() {
                const targetContent = document.querySelector(`[data-strand-content="${this.getAttribute('data-strand')}"]`);
                targetContent.style.display = targetContent.style.display === 'none' ? '' : 'none';
            });

            gridContainer.appendChild(strandHeader);
            gridContainer.appendChild(strandContent);
        }

        if (row.topic_title !== currentTopic) {
            currentTopic = row.topic_title;
            topicCounter++;
            topicDiv = document.createElement('div');
            topicDiv.className = 'topic-container content';
            topicDiv.setAttribute('data-topic', topicCounter);

            const topicHeader = document.createElement('h3');
            topicHeader.className = 'topic-subheader collapsible';
            topicHeader.textContent = currentTopic;
            topicHeader.setAttribute('data-topic', topicCounter);

            list = document.createElement('ul');
            list.className = 'subtopic-list';

            topicHeader.addEventListener('click', function() {
                const targetList = document.querySelector(`[data-topic="${this.getAttribute('data-topic')}"] .subtopic-list`);
                targetList.style.display = targetList.style.display === 'none' ? '' : 'none';
            });

            topicDiv.appendChild(topicHeader);
            topicDiv.appendChild(list);
            const targetStrandContent = document.querySelector(`[data-strand-content="${strandCounter}"]`);
            targetStrandContent.appendChild(topicDiv);
        }

        const listItem = document.createElement('li');
        listItem.className = 'subtopic-item';
        listItem.textContent = row.subtopic_title;
        list.appendChild(listItem);
    });
}

