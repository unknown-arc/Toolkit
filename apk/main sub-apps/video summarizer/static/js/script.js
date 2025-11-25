class VideoSummarizerApp {
    constructor() {
        this.currentFile = null;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File upload
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('videoFile');

        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        uploadArea.addEventListener('drop', (e) => this.handleFileDrop(e));
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Process button
        document.getElementById('processBtn').addEventListener('click', () => this.processVideo());

        // New summary button
        document.getElementById('newSummary').addEventListener('click', () => this.resetForm());

        // Add keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.style.background = '#eef2ff';
        e.currentTarget.style.borderColor = '#764ba2';
        e.currentTarget.classList.add('pulse');
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.currentTarget.style.background = '#f8f9ff';
        e.currentTarget.style.borderColor = '#667eea';
        e.currentTarget.classList.remove('pulse');
    }

    handleFileDrop(e) {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
        e.currentTarget.style.background = '#f8f9ff';
        e.currentTarget.style.borderColor = '#667eea';
        e.currentTarget.classList.remove('pulse');
        e.currentTarget.classList.add('success');
        setTimeout(() => {
            e.currentTarget.classList.remove('success');
        }, 2000);
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
            const uploadArea = document.getElementById('uploadArea');
            uploadArea.classList.add('success');
            setTimeout(() => {
                uploadArea.classList.remove('success');
            }, 2000);
        }
    }

    handleKeyboardShortcuts(e) {
        // Ctrl + O to open file dialog
        if (e.ctrlKey && e.key === 'o') {
            e.preventDefault();
            document.getElementById('videoFile').click();
        }
        
        // Enter to process when file is selected
        if (e.key === 'Enter' && this.currentFile && !document.getElementById('processBtn').disabled) {
            this.processVideo();
        }
        
        // Escape to reset form
        if (e.key === 'Escape') {
            this.resetForm();
        }
    }

    handleFile(file) {
        // Validate file type
        const validTypes = ['.mp4', '.avi', '.mov', '.mkv', '.webm'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!validTypes.includes(fileExtension)) {
            this.showError('Please select a valid video file (MP4, AVI, MOV, MKV, WEBM)');
            return;
        }

        // Validate file size (100MB limit)
        if (file.size > 100 * 1024 * 1024) {
            this.showError('File size must be less than 100MB');
            return;
        }

        this.currentFile = file;
        
        document.getElementById('fileInfo').textContent = `Selected: ${file.name} (${this.formatFileSize(file.size)})`;
        document.getElementById('fileInfo').style.color = '#28a745';
        this.updateProcessButton();
        
        // Auto-scroll to settings
        setTimeout(() => {
            document.querySelector('.settings').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }, 500);
    }

    async processVideo() {
        const processBtn = document.getElementById('processBtn');
        const loadingDiv = document.getElementById('loading');
        const resultsDiv = document.getElementById('results');
        const errorDiv = document.getElementById('error');

        // Hide previous results and errors
        resultsDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');

        // Show loading
        loadingDiv.classList.remove('hidden');
        processBtn.disabled = true;

        // Update progress steps
        this.updateProgressSteps(0);

        try {
            const formData = new FormData();
            const summaryLength = document.getElementById('summaryLength').value;
            const useAI = document.getElementById('useAI').checked;

            if (!this.currentFile) {
                throw new Error('Please select a video file first');
            }

            formData.append('file', this.currentFile);
            formData.append('summary_length', summaryLength);
            formData.append('use_ai', useAI);

            const response = await fetch('/api/summarize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'An error occurred while processing the video');
            }

            this.displayResults(data);

        } catch (error) {
            this.showError(error.message);
        } finally {
            loadingDiv.classList.add('hidden');
            this.updateProcessButton();
        }
    }

    updateProgressSteps(step) {
        const steps = document.querySelectorAll('.step');
        steps.forEach((s, index) => {
            if (index <= step) {
                s.classList.add('active');
            } else {
                s.classList.remove('active');
            }
        });
    }

    displayResults(data) {
        document.getElementById('summaryText').textContent = data.summary;
        document.getElementById('videoDuration').textContent = data.duration;
        document.getElementById('processingTime').textContent = `${data.processing_time}s`;
        document.getElementById('wordCount').textContent = data.word_count;
        
        if (data.transcript) {
            document.getElementById('transcriptText').textContent = data.transcript;
        }

        document.getElementById('results').classList.remove('hidden');
        
        // Scroll to results
        document.getElementById('results').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    resetForm() {
        // Reset file upload
        this.currentFile = null;
        
        document.getElementById('videoFile').value = '';
        document.getElementById('fileInfo').textContent = '';
        document.getElementById('fileInfo').style.color = '#667eea';
        
        // Hide results and errors
        document.getElementById('results').classList.add('hidden');
        document.getElementById('error').classList.add('hidden');
        
        this.updateProcessButton();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    updateProcessButton() {
        const processBtn = document.getElementById('processBtn');
        processBtn.disabled = !this.currentFile;
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        const errorText = document.getElementById('errorText');
        
        errorText.textContent = message;
        errorDiv.classList.remove('hidden');
        
        errorDiv.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new VideoSummarizerApp();
    
    // Add some helpful tips
    console.log('💡 Keyboard shortcuts:');
    console.log('   Ctrl + O - Open file dialog');
    console.log('   Enter - Process video (when file selected)');
    console.log('   Escape - Reset form');
});
