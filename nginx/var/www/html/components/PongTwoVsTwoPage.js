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

    const players = {
        player1: 'Player 1',
        player2: 'Player 2',
        player3: 'Player 3',
        player4: 'Player 4'
    };

    const game = new PongGame(container, players);
    return container;
}