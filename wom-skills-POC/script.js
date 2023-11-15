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
    let counter = 0;

    data.forEach(row => {
        if (row.Strand !== currentStrand) {
            currentStrand = row.Strand;
            const strandHeader = document.createElement('h2');
            strandHeader.className = 'strand-header collapsible';
            strandHeader.textContent = currentStrand;
            strandHeader.setAttribute('data-target', counter);

            const strandContent = document.createElement('div');
            strandContent.className = 'content';
            strandContent.setAttribute('data-content', counter);

            strandHeader.addEventListener('click', function() {
                const targetContent = document.querySelector(`[data-content="${this.getAttribute('data-target')}"]`);
                targetContent.style.display = targetContent.style.display === 'none' ? '' : 'none';
            });

            gridContainer.appendChild(strandHeader);
            gridContainer.appendChild(strandContent);
            counter++;
        }

        if (row.topic_title !== currentTopic) {
            currentTopic = row.topic_title;
            topicDiv = document.createElement('div');
            topicDiv.className = 'topic-container content';
            topicDiv.setAttribute('data-target', counter);

            const topicHeader = document.createElement('h3');
            topicHeader.className = 'topic-subheader collapsible';
            topicHeader.textContent = currentTopic;
            topicHeader.setAttribute('data-target', counter);

            list = document.createElement('ul');
            list.className = 'subtopic-list';

            topicHeader.addEventListener('click', function() {
                const targetList = document.querySelector(`[data-content="${this.getAttribute('data-target')}"]`);
                targetList.style.display = targetList.style.display === 'none' ? '' : 'none';
            });

            topicDiv.appendChild(topicHeader);
            topicDiv.appendChild(list);
            const targetStrandContent = document.querySelector(`[data-content="${counter - 1}"]`);
            targetStrandContent.appendChild(topicDiv);
            counter++;
        }

        const listItem = document.createElement('li');
        listItem.className = 'subtopic-item';
        listItem.textContent = row.subtopic_title;
        list.appendChild(listItem);
    });
}
