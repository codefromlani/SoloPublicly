document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const registerBtn = document.getElementById('registerBtn');
        const spinner = document.getElementById('spinner');
        registerBtn.disabled = true;
        spinner.style.display = 'inline-block';
        registerBtn.textContent = 'Registering...';

        document.querySelectorAll('.error-message').forEach(el => {
            el.textContent ='';
        })

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
            spinner.style.display = 'none';
            registerBtn.disabled = false;
            registerBtn.textContent = 'Register';
            return;
        }

        try {
            const response = await fetch('api/v1/users/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    email,
                    password,
                    role: 'user'
                })
            });

            const data = await response.json();

            if (!response.ok) {
                if (data.detail) {
                    if (data.detail.includes('credentials already exists')) {
                        if (data.detail.includes('username')) {
                            document.getElementById('usernameError').textContent = 'Username already taken';
                        } else {
                            document.getElementById('emailError').textContent = 'Email already taken';
                        }
                    } else {
                        alert(data.detail);
                    }
                }
                return;
            }
            
            document.getElementById('successModal').style.display = 'block';

            document.getElementById('registerForm').reset();
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during registration');
        } finally {
            spinner.style.display = 'none';
            registerBtn.disabled = false;
            registerBtn.textContent = 'Register';
        }
    });

    window.onclick = function(event) {
        const modal = document.getElementById('successModal');
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    window.addEventListener('load', () => {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');

        if (token) {
            verifyEmail(token);
        }
    });

    async function verifyEmail(token) {
        try {
            const response = await fetch(`api/v1/users/verify-email?token=${token}`, {
                method: 'GET'
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Email verification failed');
            }

            window.location.href = '/login.html';
        } catch (error) {
            alert('Email verification failed: ' + error.message);
        }
    }

    function closeModal() {
        document.getElementById('successModal').style.display = 'none';
    }