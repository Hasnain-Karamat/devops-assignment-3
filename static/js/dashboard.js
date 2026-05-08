// Dashboard interactive features
document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskForm');
    const taskInput = document.getElementById('title');
    const taskList = document.querySelector('.task-list');
    
    // Handle task form submission with animation
    if (taskForm) {
        taskForm.addEventListener('submit', function(e) {
            const submitBtn = document.getElementById('add-task-btn');
            
            // Add loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';
        });
    }
    
    // Add task input animations
    if (taskInput) {
        taskInput.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        taskInput.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
        
        // Character counter and validation
        taskInput.addEventListener('input', function() {
            const length = this.value.length;
            const submitBtn = document.getElementById('add-task-btn');
            
            if (length > 0) {
                submitBtn.style.transform = 'scale(1.05)';
                this.style.borderColor = 'var(--primary-color)';
            } else {
                submitBtn.style.transform = 'scale(1)';
                this.style.borderColor = 'var(--border-color)';
            }
            
            // Add shake animation for empty submission attempt
            if (length === 0 && this.classList.contains('shake')) {
                this.classList.remove('shake');
            }
        });
    }
    
    // Add hover effects to task items
    const taskItems = document.querySelectorAll('.task-item');
    taskItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0) scale(1)';
        });
    });
    
    // Add delete confirmation with animation
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this task?')) {
                e.preventDefault();
                return;
            }
            
            // Add fade out animation before deletion
            const taskItem = this.closest('.task-item');
            taskItem.style.transition = 'all 0.3s ease-out';
            taskItem.style.opacity = '0';
            taskItem.style.transform = 'translateX(-20px)';
        });
    });
    
    // Add task counter animation
    const taskCount = document.querySelector('.task-count');
    if (taskCount) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                taskCount.style.transform = 'scale(1.2)';
                taskCount.style.transition = 'transform 0.3s ease-out';
                setTimeout(() => {
                    taskCount.style.transform = 'scale(1)';
                }, 300);
            });
        });
        
        observer.observe(taskCount, { childList: true });
    }
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus task input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (taskInput) {
                taskInput.focus();
                taskInput.select();
            }
        }
        
        // Escape to blur input
        if (e.key === 'Escape') {
            if (document.activeElement.classList.contains('form-input')) {
                document.activeElement.blur();
            }
        }
    });
    
    // Add page visibility handling
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            // Refresh task count when page becomes visible again
            const currentCount = document.querySelectorAll('.task-item').length;
            if (taskCount) {
                taskCount.textContent = `${currentCount} ${currentCount === 1 ? 'task' : 'tasks'}`;
            }
        }
    });
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add ripple effect CSS dynamically
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .shake {
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);
