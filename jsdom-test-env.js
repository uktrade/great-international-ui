const Environment = require('jest-environment-jsdom');

module.exports = class CustomTestEnvironment extends Environment {
    async setup() {
        await super.setup();
        if (typeof this.global.TextEncoder === 'undefined') {
            const {TextEncoder} = require('util');
            this.global.TextEncoder = TextEncoder;
        }
        if (typeof this.global.TextDecoder === 'undefined') {
            const {TextDecoder} = require('util');
            this.global.TextDecoder = TextDecoder;
        }
    }
}
