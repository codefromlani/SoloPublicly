async function verifyEmail() {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');

        if (!token) {
            const pathParts = window.location.pathname.split('/');
            if (pathParts.length > 0) {
                token = pathParts[pathParts.length - 1];
            }
        }

        if (!token) {
        showError('Verification token is missing');
        return;
    }

    try {
        const response = await fetch(`/api/v1/users/verify-email?token=${token}`, {
            method: 'GET'
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Email verification failed');
        }

        showSuccess('Email verified successfully! Redirecting to login...');

        setTimeout(() => {
            window.location.href = '/login?verified=true';
        }, 2000);
    } catch (error) {
        showError(error.message);
    }
}

function showError(message) {
    const verificationStatus = document.querySelector('.verification-status');
    verificationStatus.innerHTML = `
        <h2 style="color: #e74c3c;">Verification Failed</h2>
        <p>${message}</p>
        <p style="margin-top: 1rem;">
            <a href="/login.html" class="btn-primary" style="text-decoration: none;">Go to Login</a>
        </p>
    `;
}

function showSuccess(message) {
    const verificationStatus = document.querySelector('.verification-status');
    verificationStatus.innerHTML = `
        <h2 style="color: #27ae60;">Success!</h2>
        <p>${message}</p>
    `;
}

document.addEventListener('DOMContentLoaded', verifyEmail); 