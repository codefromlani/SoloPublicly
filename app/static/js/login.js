document.addEventListener('DOMContentLoaded', () => {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('verified') === 'true') {
            document.getElementById('verificationSuccess').style.display = 'block';
        }
    });

    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const formData = new URLSearchParams();
        formData.append('username', email);  
        formData.append('password', password);

        hideMessages();

        try {
            const response = await fetch('api/v1/users/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                if (response.status === 400 && data.detail === "Please verify your email before logging in") {

                    document.getElementById('verificationNotice').style.display = 'block';

                    localStorage.setItem('pendingVerificationEmail', email);
                } else {
                    const loginError = document.getElementById('loginError');
                    loginError.textContent = data.detail || 'Login failed';
                    loginError.style.display = 'block';

                }
                return;
            }

            localStorage.setItem('token', data.access_token);

            window.location.href = '/dashboard';
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('loginError').textContent = 'An error occurred during login';
        }
    });

    document.getElementById('resendVerification').addEventListener('click', async (e) => {
        e.preventDefault();

        const email = localStorage.getItem('pendingVerificationEmail');
        if (!email) {
            showError('Email not found. Please try logging in again.');
            return;
        }

        const loader = document.getElementById('resendLoader');
        loader.style.display = 'inline-block';

        try {
            const response = await fetch('api/v1/users/resend-verification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.detail || 'Failed to resend verification email');
                return;
            } 

            document.getElementById('resendSuccess').style.display = 'block';

            document.getElementById('verificationNotice').style.display = 'none';
        } catch(error) {
            if (error instanceof Error) {
                showError(error.message);
            } else {
                showError('An unexpected error occurred.');
            }
        } finally {
            loader.style.display = 'none';
        }
    });

    function showError(message) {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.getElementById('loginForm').appendChild(errorDiv);
    }

    function hideMessages() {
    document.getElementById('verificationNotice').style.display = 'none';
    document.getElementById('resendSuccess').style.display = 'none';
    
    const loginError = document.getElementById('loginError');
    if (loginError) {
        loginError.textContent = '';
        loginError.style.display = 'none';
    }
}
