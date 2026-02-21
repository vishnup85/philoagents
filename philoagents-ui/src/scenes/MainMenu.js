import {Scene} from 'phaser';

export class MainMenu extends Scene {
    constructor() {
        super('MainMenu');
    }

    create() {
        this.add.text(400, 350, 'PhiloAgents Menu', { fill: '#ffffff' });
    }
}