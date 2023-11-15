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
    let currentTopicId = '';

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

        if (row.topic_id !== currentTopicId) {
            currentTopicId = row.topic_id;
            const topicDiv = document.createElement('div');
            topicDiv.className = 'topic-container content';

            const topicHeader = document.createElement('h3');
            topicHeader.className = 'topic-subheader collapsible';
            topicHeader.textContent = row.topic_title;
            topicHeader.setAttribute('data-topic', currentTopicId);

            const list = document.createElement('ul');
            list.className = 'subtopic-list';
            topicHeader.addEventListener('click', function() {
                const targetList = document.querySelector(`[data-topic="${currentTopicId}"] .subtopic-list`);
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
