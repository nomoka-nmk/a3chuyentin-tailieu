let allDocuments = [];

document.addEventListener('DOMContentLoaded', async function() {
    allDocuments = await loadDocuments();
    setupSearch();
});

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    
    searchInput.addEventListener('input', function() {
        performDynamicSearch(this.value.trim());
    });
    
    searchInput.focus();
}

function performDynamicSearch(query) {
    if (!query) {
        displayDocuments(allDocuments);
        updateSearchTitle('Tất cả tài liệu', allDocuments.length);
        return;
    }

    const normalizedQuery = query.toLowerCase();
    const results = allDocuments.filter(doc => {
        const searchFields = [
            doc.displayName,
            doc.description,
            ...(doc.tags || [])
        ];
        
        return searchFields.some(field => 
            field && field.toLowerCase().includes(normalizedQuery)
        );
    });

    displayDocuments(results);
    updateSearchTitle(`Đang tìm: "${query}"`, results.length);
}

async function loadDocuments() {
    const spinner = document.getElementById('loading-spinner');
    spinner.classList.remove('hidden');
    
    try {
        const response = await fetch('./assets/documents/documents.json');
        const documents = await response.json();
        displayDocuments(documents);
        return documents;
    } catch (error) {
        console.error('Error loading documents:', error);
        document.getElementById('documents-grid').innerHTML = `
            <div class="col-span-full text-center py-8">
                <i class="fas fa-exclamation-triangle text-4xl text-red-500 mb-4"></i>
                <p class="text-xl text-gray-700">Không thể tải tài liệu. Vui lòng thử lại sau.</p>
            </div>
        `;
        return [];
    } finally {
        spinner.classList.add('hidden');
    }
}

function performSearch(documents) {
    const query = document.getElementById('search-input').value.trim().toLowerCase();
    
    if (!query) {
        displayDocuments(documents);
        updateSearchTitle('Tất cả tài liệu', documents.length);
        return;
    }
    
    const results = documents.filter(doc => {
        const searchInName = doc.displayName.toLowerCase().includes(query);
        const searchInDesc = doc.description && doc.description.toLowerCase().includes(query);
        const searchInTags = doc.tags && doc.tags.some(tag => tag.toLowerCase().includes(query));
        
        return searchInName || searchInDesc || searchInTags;
    });
    
    displayDocuments(results);
    updateSearchTitle(`Kết quả tìm kiếm cho "${query}"`, results.length);
}

function updateSearchTitle(title, count) {
    const gridTitle = document.querySelector('section:last-child h2');
    if (gridTitle) {
        gridTitle.textContent = `${title} (${count})`;
    }
}