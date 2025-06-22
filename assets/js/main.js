function initDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    
    if (isDarkMode) {
        document.documentElement.classList.add('dark');
    }
    
    darkModeToggle.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', isDark);
    });
}

let allDocuments = [];

document.addEventListener('DOMContentLoaded', function() {
    initDarkMode();
    loadDocuments().then(docs => {
        allDocuments = docs;
        setupSearch();
    });
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
        updateSearchTitle('Tất cả tài liệu');
        return;
    }

    const normalizedQuery = query.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const results = allDocuments.filter(doc => {
        const searchFields = [
            doc.displayName,
            doc.description,
            ...(doc.tags || [])
        ];
        
        return searchFields.some(field => 
            field && field.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(normalizedQuery)
        );
    });

    displayDocuments(results);
    updateSearchTitle(`Kết quả tìm kiếm: "${query}"`);
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
                <p class="text-xl text-gray-700 dark:text-gray-300">Không thể tải tài liệu. Vui lòng thử lại sau.</p>
            </div>
        `;
        return [];
    } finally {
        spinner.classList.add('hidden');
    }
}

function displayDocuments(documents) {
    const grid = document.getElementById('documents-grid');
    grid.innerHTML = '';
    
    if (documents.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-folder-open text-5xl text-gray-300 dark:text-gray-600 mb-4"></i>
                <p class="text-xl text-gray-600 dark:text-gray-300 mb-2">Không tìm thấy tài liệu phù hợp</p>
                <p class="text-gray-500 dark:text-gray-400">Thử với từ khóa tìm kiếm khác</p>
            </div>
        `;
        return;
    }
    
    documents.sort((a, b) => new Date(b.uploadDate) - new Date(a.uploadDate)).forEach((doc, index) => {
        const icon = getFileIcon(doc.type);
        const colors = getFileTypeColors(doc.type);
        const filePath = `https://chuyentin-tailieu.a3sachhonaba.com/assets/documents/files/${doc.fileName}.html`;

        const card = document.createElement('div');
        card.className = 'document-card bg-white dark:bg-[#111111] rounded-xl overflow-hidden shadow-md dark:shadow-none border border-gray-100 dark:border-gray-800';
        card.dataset.id = doc.id;
        card.style.animationDelay = `${index * 0.05}s`;

        card.innerHTML = `
            <div class="document-card-content p-6">
                <div class="flex items-start mb-4">
                    <div class="file-type-badge ${colors.bg} ${colors.text} shadow-sm">
                        <i class="${icon} text-xl"></i>
                    </div>
                    <div class="ml-4 flex-1">
                        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 line-clamp-1">${doc.displayName}</h3>
                        <div class="flex items-center mt-1">
                            <span class="text-xs font-medium px-2 py-1 rounded-full ${colors.bg} ${colors.text}">
                                ${formatFileType(doc.type)}
                            </span>
                            <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">
                                ${formatDate(doc.uploadDate)}
                            </span>
                        </div>
                    </div>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm line-clamp-2 mb-4">${doc.description || 'Không có mô tả'}</p>
            </div>
        `;
        
        card.addEventListener('click', () => {
            window.open(filePath, '_blank');
        });
        
        grid.appendChild(card);
    });
}

function getFileIcon(fileType) {
    const type = fileType.split('/')[0];
    switch(type) {
        case 'application':
            if (fileType.includes('pdf')) return 'fas fa-file-pdf';
            if (fileType.includes('word') || fileType.includes('msword')) return 'fas fa-file-word';
            if (fileType.includes('excel') || fileType.includes('spreadsheet')) return 'fas fa-file-excel';
            if (fileType.includes('powerpoint') || fileType.includes('presentation')) return 'fas fa-file-powerpoint';
            if (fileType.includes('zip') || fileType.includes('compressed')) return 'fas fa-file-archive';
            return 'fas fa-file-alt';
        case 'text':
            return 'fas fa-file-alt';
        case 'image':
            return 'fas fa-file-image';
        default:
            return 'fas fa-file';
    }
}

function getFileTypeColors(fileType) {
    const type = fileType.split('/')[0];
    switch(type) {
        case 'application':
            if (fileType.includes('pdf')) return { bg: 'bg-red-100 dark:bg-red-900', text: 'text-red-600 dark:text-red-200' };
            if (fileType.includes('word') || fileType.includes('msword')) return { bg: 'bg-blue-100 dark:bg-blue-900', text: 'text-blue-600 dark:text-blue-200' };
            if (fileType.includes('excel') || fileType.includes('spreadsheet')) return { bg: 'bg-green-100 dark:bg-green-900', text: 'text-green-600 dark:text-green-200' };
            if (fileType.includes('powerpoint') || fileType.includes('presentation')) return { bg: 'bg-orange-100 dark:bg-orange-900', text: 'text-orange-600 dark:text-orange-200' };
            if (fileType.includes('zip') || fileType.includes('compressed')) return { bg: 'bg-purple-100 dark:bg-purple-900', text: 'text-purple-600 dark:text-purple-200' };
            return { bg: 'bg-gray-100 dark:bg-gray-700', text: 'text-gray-600 dark:text-gray-200' };
        case 'text':
            return { bg: 'bg-gray-100 dark:bg-gray-700', text: 'text-gray-600 dark:text-gray-200' };
        case 'image':
            return { bg: 'bg-pink-100 dark:bg-pink-900', text: 'text-pink-600 dark:text-pink-200' };
        default:
            return { bg: 'bg-gray-100 dark:bg-gray-700', text: 'text-gray-600 dark:text-gray-200' };
    }
}

function formatFileType(fileType) {
    const type = fileType.split('/')[0];
    switch(type) {
        case 'application':
            if (fileType.includes('pdf')) return 'PDF';
            if (fileType.includes('word') || fileType.includes('msword')) return 'Word';
            if (fileType.includes('excel') || fileType.includes('spreadsheet')) return 'Excel';
            if (fileType.includes('powerpoint') || fileType.includes('presentation')) return 'PowerPoint';
            if (fileType.includes('zip') || fileType.includes('compressed')) return 'Tệp nén';
            return 'Tài liệu';
        case 'text':
            return 'Văn bản';
        case 'image':
            return 'Hình ảnh';
        default:
            return 'Tệp';
    }
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('vi-VN', options);
}

function updateSearchTitle(title) {
    const titleElement = document.getElementById('documents-title');
    if (titleElement) {
        titleElement.innerHTML = `<i class="fas fa-book-open text-blue-500 mr-2"></i>${title}`;
    }
}