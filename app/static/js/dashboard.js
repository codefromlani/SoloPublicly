document.addEventListener('DOMContentLoaded', async function() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    try {
        const userResponse = await fetch('/api/v1/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!userResponse.ok) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }
        
        const userData = await userResponse.json();
        
        document.getElementById('dashboardGreeting').textContent = `Welcome, ${userData.username}`;
        
        const projectsResponse = await fetch('/api/v1/projects/all', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (projectsResponse.ok) {
            const projects = await projectsResponse.json();
            const projectsContainer = document.getElementById('recentProjects');
            
            if (projects.length === 0) {
                projectsContainer.innerHTML = `
                    <p>You don't have any projects yet. <a href="/projects/create" style="color: var(--secondary-color);">Create your first project</a>.</p>
                `;
            } else {
                let projectsHTML = `
                    <div class="project-list">
                `;
                
                projects.forEach(project => {
                    const statusClass = getStatusClass(project.status);
                    const formattedDate = new Date(project.updated_at).toLocaleDateString();
                    
                    projectsHTML += `
                        <div class="project-card">
                            <div class="project-header">
                                <h3>${project.title}</h3>
                                <span class="status-badge ${statusClass}">${project.status}</span>
                            </div>
                            <p class="project-description">${project.description || 'No description provided'}</p>
                            <div class="project-tags">
                                ${project.tags && project.tags.length ? project.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : '<span class="no-tags">No tags</span>'}
                            </div>
                            <div class="project-footer">
                                <span class="project-date">Updated: ${formattedDate}</span>
                                <div class="project-actions">
                                    <a href="/projects/view/${project.id}" class="btn-small">View</a>
                                    <a href="/projects/edit/${project.id}" class="btn-small">Edit</a>
                                    <button class="btn-small btn-danger" onclick="deleteProject('${project.id}', '${project.title}')">Delete</button>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                projectsHTML += `</div>`;
                projectsContainer.innerHTML = projectsHTML;
            }
        } else {
            document.getElementById('recentProjects').innerHTML = `
                <div class="error-message">
                    Failed to load projects
                </div>
            `;
        }
    } catch (error) {
        console.error('Error fetching data:', error);

        document.getElementById('recentProjects').innerHTML = `
            <div class="error-message">
                Failed to load projects
            </div>
        `;
    }
});

function getStatusClass(status) {
    switch (status) {
        case 'idea':
            return 'status-idea';
        case 'in_progress':
            return 'status-progress';
        case 'done':
            return 'status-done';
        default:
            return '';
    }
}

function deleteProject(projectId, projectTitle) {
    if (confirm(`Are you sure you want to delete "${projectTitle}"? This action cannot be undone.`)) {
        const token = localStorage.getItem('token');
        
        fetch(`/api/v1/projects/delete/${projectId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Failed to delete project. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error deleting project:', error);
            alert('An error occurred while deleting the project.');
        });
    }
}