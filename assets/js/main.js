document.addEventListener('DOMContentLoaded', function() {
    fetch('./components/header.html')
        .then(response => response.text())
        .then(data => document.getElementById('header-container').innerHTML = data);
    
    fetch('./components/footer.html')
        .then(response => response.text())
        .then(data => document.getElementById('footer-container').innerHTML = data);
    
    loadDocuments();
});

async function loadDocuments() {
    const spinner = document.getElementById('loading-spinner');
    spinner.classList.remove('hidden');
    
    try {
        const response = await fetch('./assets/documents/documents.json');
        const documents = await response.json();
        
        displayDocuments(documents);
    } catch (error) {
        console.error('Error loading documents:', error);
        document.getElementById('documents-grid').innerHTML = `
            <div class="col-span-full text-center py-8">
                <i class="fas fa-exclamation-triangle text-4xl text-red-500 mb-4"></i>
                <p class="text-xl text-gray-700">Không thể tải tài liệu. Vui lòng thử lại sau.</p>
            </div>
        `;
    } finally {
        spinner.classList.add('hidden');
    }
}

function displayDocuments(documents) {
    
    const grid = document.getElementById('documents-grid');
    grid.innerHTML = '';
    
    if (documents.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-8">
                <i class="fas fa-folder-open text-4xl text-gray-400 mb-4"></i>
                <p class="text-xl text-gray-700">Không tìm thấy tài liệu phù hợp</p>
            </div>
        `;
        return;
    }
    
    documents.forEach(doc => {
        
        const icon = getFileIcon(doc.type);
        const colors = getFileTypeColors(doc.type);
        
        const card = document.createElement('div');
        card.className = 'bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1 cursor-pointer';
        card.dataset.id = doc.id;

        const filePath = `${window.location.origin}/assets/documents/files/${doc.fileName}`;

        card.innerHTML = `
            <div class="p-6">
                <div class="flex items-center mb-4">
                    <div class="${colors.bg} ${colors.text} rounded-lg p-3 mr-4">
                        <i class="${icon} fa-lg"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-gray-800 line-clamp-1">${doc.displayName}</h3>
                        <p class="text-sm text-gray-500">${formatFileType(doc.type)}</p>
                    </div>
                </div>
                <p class="text-gray-600 text-sm line-clamp-2 mb-4">${doc.description || 'Không có mô tả'}</p>
                <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-400">${formatDate(doc.uploadDate)}</span>
                    <a href="/viewer/viewer.html?url=${encodeURIComponent(filePath)}" 
                       target="_blank"
                       class="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
                       onclick="event.stopPropagation()">
                        Xem tài liệu <i class="fas fa-chevron-right ml-1"></i>
                    </a>
                </div>
            </div>
        `;
        
        card.addEventListener('click', () => {
            window.open(`/viewer/viewer.html?url=${encodeURIComponent(filePath)}`, '_blank');
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

document.addEventListener('DOMContentLoaded', function() {
    fetch('./components/header.html')
        .then(response => response.text())
        .then(data => document.getElementById('header-container').innerHTML = data);
    
    fetch('./components/footer.html')
        .then(response => response.text())
        .then(data => document.getElementById('footer-container').innerHTML = data);
});

function getFileTypeColors(fileType) {
    const type = fileType.split('/')[0];
    switch(type) {
        case 'application':
            if (fileType.includes('pdf')) return { bg: 'bg-red-100', text: 'text-red-600' };
            if (fileType.includes('word') || fileType.includes('msword')) return { bg: 'bg-blue-100', text: 'text-blue-600' };
            if (fileType.includes('excel') || fileType.includes('spreadsheet')) return { bg: 'bg-green-100', text: 'text-green-600' };
            if (fileType.includes('powerpoint') || fileType.includes('presentation')) return { bg: 'bg-orange-100', text: 'text-orange-600' };
            if (fileType.includes('zip') || fileType.includes('compressed')) return { bg: 'bg-purple-100', text: 'text-purple-600' };
            return { bg: 'bg-gray-100', text: 'text-gray-600' };
        case 'text':
            return { bg: 'bg-gray-100', text: 'text-gray-600' };
        case 'image':
            return { bg: 'bg-pink-100', text: 'text-pink-600' };
        default:
            return { bg: 'bg-gray-100', text: 'text-gray-600' };
    }
}

function formatFileType(fileType) {
    const type = fileType.split('/')[0];
    switch(type) {
        case 'application':
            if (fileType.includes('pdf')) return 'Tài liệu PDF';
            if (fileType.includes('word') || fileType.includes('msword')) return 'Tài liệu Word';
            if (fileType.includes('excel') || fileType.includes('spreadsheet')) return 'Bảng tính Excel';
            if (fileType.includes('powerpoint') || fileType.includes('presentation')) return 'Trình chiếu PowerPoint';
            if (fileType.includes('zip') || fileType.includes('compressed')) return 'Tệp nén';
            return 'Tài liệu';
        case 'text':
            return 'Tệp văn bản';
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