// Authentication form interactions
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const submitBtn = document.getElementById('login-btn');
            const btnText = document.getElementById('btn-text');
            const spinner = submitBtn.querySelector('.spinner');
            
            // Show loading state
            btnText.style.display = 'none';
            spinner.style.display = 'inline-block';
            submitBtn.disabled = true;
            
            // Add some visual feedback
            submitBtn.style.opacity = '0.7';
        });
    }
    
    // Handle register form submission
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const submitBtn = document.getElementById('register-btn');
            const btnText = document.getElementById('btn-text');
            const spinner = submitBtn.querySelector('.spinner');
            
            // Show loading state
            btnText.style.display = 'none';
            spinner.style.display = 'inline-block';
            submitBtn.disabled = true;
            
            // Add some visual feedback
            submitBtn.style.opacity = '0.7';
        });
    }
    
    // Add input animations
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Add character counter for password fields
        if (input.type === 'password') {
            input.addEventListener('input', function() {
                const length = this.value.length;
                if (length > 0) {
                    this.style.borderColor = length >= 6 ? 'var(--secondary-color)' : 'var(--border-color)';
                }
            });
        }
    });
    
    // Add floating label effect
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        const input = group.querySelector('.form-input');
        const label = group.querySelector('.form-label');
        
        if (input && label) {
            input.addEventListener('focus', () => {
                label.style.color = 'var(--primary-color)';
                label.style.transform = 'translateY(-2px)';
            });
            
            input.addEventListener('blur', () => {
                label.style.color = 'var(--text-primary)';
                label.style.transform = 'translateY(0)';
            });
        }
    });
});
