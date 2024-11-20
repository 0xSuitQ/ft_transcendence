// header.js
import { state, setLoggedIn } from './utils/state.js';
import { loadAllStyles } from './utils/loadCSS.js';
import { logout } from './utils/auth.js';

export async function header() {
    await loadAllStyles();

    const headerElement = document.createElement('header');
    headerElement.className = 'header';

    const navButtons = document.createElement('div');
    navButtons.className = 'nav-buttons';
    ['Home', 'Profile', 'Games', 'Tournament'].forEach(num => {
        const button = document.createElement('button');
        button.innerText = num;
        button.className = 'nav-button';
        if (num === 'Home') {
            button.addEventListener('click', () => {
                navigateTo('/');
            });
        } else if (num === 'Tournament') {
            button.addEventListener('click', () => {
                navigateTo('/tournament');
            });
        } else if (num === 'Profile') {
            button.addEventListener('click', () => {
                navigateTo('/profile');
            });
        } else if (num === 'Games') {
            button.addEventListener('click', () => {
                navigateTo('/game');
            });
        }
        navButtons.appendChild(button);
    });

    const userSection = document.createElement('div');
    userSection.className = 'user-section';

    if (state.isLoggedIn) {
        const logoutButton = document.createElement('button');
        logoutButton.innerText = 'Log out';
        logoutButton.className = 'auth-button';
        logoutButton.onclick = logout;
        userSection.appendChild(logoutButton);
    }

    headerElement.appendChild(navButtons);
    headerElement.appendChild(userSection);

    // Add class to hide header if not logged in
    if (!state.isLoggedIn) {
        headerElement.classList.add('hidden');
    }

    return headerElement;
}
