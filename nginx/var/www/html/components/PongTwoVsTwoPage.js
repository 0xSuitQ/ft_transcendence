// PongTwoVsTwoPage.js
import { PongGame } from './PongGame.js';
import { checkLoginStatus } from './utils/state.js';

export async function PongTwoVsTwoPage() {
    if (!checkLoginStatus()) {
        window.navigateTo('/');
        return document.createElement('div');
    }

    const container = document.createElement('div');
    container.className = 'match-container';

    let currentUserId;
    let currentUsername;
    try {
        const response = await fetch('/api/profiles/me/', {
            credentials: 'include'
        });
        const userData = await response.json();
        currentUserId = userData.user.id;
        currentUsername = userData.user.username;

        const setupForm = document.createElement('form');
        setupForm.className = 'player-setup-form';

        const player1Input = document.createElement('input');
        player1Input.type = 'text';
        player1Input.value = currentUsername;
        player1Input.disabled = true;

        const player2Input = document.createElement('input');
        player2Input.type = 'text';
        player2Input.placeholder = 'Enter Player 2 name';
        player2Input.required = true;

        const player3Input = document.createElement('input');
        player3Input.type = 'text';
        player3Input.placeholder = 'Enter Player 3 name';
        player3Input.required = true;

        const player4Input = document.createElement('input');
        player4Input.type = 'text';
        player4Input.placeholder = 'Enter Player 4 name';
        player4Input.required = true;

        const startButton = document.createElement('button');
        startButton.type = 'submit';
        startButton.textContent = 'Start Game';

        setupForm.appendChild(createInputGroup('Player 1:', player1Input));
        setupForm.appendChild(createInputGroup('Player 2:', player2Input));
        setupForm.appendChild(createInputGroup('Player 3:', player3Input));
        setupForm.appendChild(createInputGroup('Player 4:', player4Input));
        setupForm.appendChild(startButton);

        container.appendChild(setupForm);

        setupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const players = {
                player1: currentUsername,
                player2: player2Input.value,
                player3: player3Input.value,
                player4: player4Input.value
            };

            setupForm.remove();

            const game = new PongGame(container, players);

            game.onGameEnd = async () => {
                try {
                    await fetch('/api/matches/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            player1: currentUserId,
                            player2: players.player2,
                            player3: players.player3,
                            player4: players.player4,
                            match_score: `${game.player1.score + game.player3.score}-${game.player2.score + game.player4.score}`
                        })
                    });
                } catch (error) {
                    console.error('Error saving match result:', error);
                }
            };
        });

    } catch (error) {
        console.error('Error fetching user data:', error);
    }

    return container;
}

function createInputGroup(label, input) {
    const group = document.createElement('div');
    group.className = 'input-group';

    const labelElement = document.createElement('label');
    labelElement.textContent = label;

    group.appendChild(labelElement);
    group.appendChild(input);

    return group;
}
