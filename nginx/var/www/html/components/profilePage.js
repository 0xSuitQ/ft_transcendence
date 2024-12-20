// profilePage.js
import { loadAllStyles } from './utils/loadCSS.js';
import { checkLoginStatus } from './utils/state.js';
import { translate } from './utils/translate.js';

import { renderUserInfo } from './profileSections/userInfoSection.js';
import { renderEmailForm } from './profileSections/emailSection.js';
import { renderPasswordForm } from './profileSections/passwordSection.js';
import { renderAddFriendForm, renderFriendList, renderPendingRequests } from './profileSections/friendsSection.js';
import { renderMatchHistory } from './profileSections/matchHistorySection.js';
import { render2FA } from './profileSections/twoFactorSection.js';
import { renderLanguageChange } from './profileSections/languageSection.js';

export async function profilePage() {
    if (!checkLoginStatus()) {
        window.navigateTo('/');
        return document.createElement('div');
    }

    await loadAllStyles();

    const container = document.createElement('div');
    container.className = 'user-container';

    // Create sidebar
    const sidebar = document.createElement('div');
    sidebar.className = 'sidebar';
    const sidebarList = document.createElement('ul');

    const sections = [
        'User Info',
        'Change Email',
        'Change Password',
        '2-Factor Authentication',
        'Add Friend',
        'Friend List',
        'Pending Requests',
        'Match History',
        'Language',
    ];

    sections.forEach(section => {
        const li = document.createElement('li');
        li.textContent = translate(section);
        li.addEventListener('click', () => showSection(section));
        sidebarList.appendChild(li);
    });

    sidebar.appendChild(sidebarList);
    container.appendChild(sidebar);

    const mainContent = document.createElement('div');
    mainContent.className = 'user-info';
    container.appendChild(mainContent);

    let userInfo = {
        username: '',
        email: '',
        avatar: '',
        wins: 0,
        losses: 0,
        cowboyWins: 0,
        cowboyLosses: 0
    };

    async function fetchUserData() {
        try {
            const response = await fetch('/api/profiles/me/', {
                credentials: 'include'
            });
            const data = await response.json();
            userInfo = {
                username: data.user.username,
                email: data.user.email,
                avatar: data.avatar,
                wins: data.wins,
                losses: data.losses,
                cowboyWins: data.cowboy_wins,
                cowboyLosses: data.cowboy_losses
            };
            showSection('User Info');
        } catch (error) {
            console.error(translate('Error fetching user data:'), error);
        }
    }

    function showSection(sectionName) {
        mainContent.innerHTML = '';

        switch (sectionName) {
            case 'User Info':
                renderUserInfo(userInfo, mainContent);
                break;
            case 'Change Email':
                renderEmailForm(userInfo, mainContent, showSection);
                break;
            case 'Change Password':
                renderPasswordForm(mainContent, showSection);
                break;
            case 'Add Friend':
                renderAddFriendForm(mainContent);
                break;
            case 'Friend List':
                renderFriendList(mainContent, userInfo, showSection);
                break;
            case 'Pending Requests':
                renderPendingRequests(mainContent, showSection);
                break;
            case 'Match History':
                renderMatchHistory(mainContent);
                break;
            case '2-Factor Authentication':
                render2FA(mainContent);
                break;
            case 'Language':
                renderLanguageChange(mainContent, showSection);
                break;
        }
    }

    await fetchUserData();

    return container;
}

