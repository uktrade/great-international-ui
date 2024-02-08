const VideoPlayerController = require('../src/dit.videoHeroControl');

describe('VideoPlayerController', () => {
    let video;
    let controlBtn;
    let videoPlayerController;
    let videoStatus;

    beforeEach(() => {
        document.body.innerHTML = `
            <video id="js-atlas-video"></video>
            <button id="js-video-control" class="atlas-hero__video-control-play">
                <span class="atlas-hero__video-control-icon"><span>Play</span></span>
            </button>
            <div id="js-video-status"></div>
        `;

        video = document.getElementById('js-atlas-video');
        controlBtn = document.getElementById('js-video-control');
        videoStatus = document.getElementById('js-video-status');
        videoPlayerController = new VideoPlayerController(video, controlBtn);

        video.play = jest.fn();
        video.pause = jest.fn();
    });

    test('should initialise with correct classes and attributes', () => {
        expect(controlBtn.classList.contains('atlas-hero__video-control-play')).toBeTruthy();
        expect(video.paused).toBeTruthy();
    });

    test('should play video when control button clicked and video is paused', () => {
        video.paused = true;
        controlBtn.click();
        expect(controlBtn.getAttribute('aria-pressed')).toBe('true');
        setTimeout(() => {
            expect(videoStatus.textContent).toBe('Video playing');
            expect(controlBtn.classList.contains('atlas-hero__video-control-pause')).toBeTruthy();
            done();
        }, 100);
    });

    test('should pause video when control button clicked and video is playing', () => {
        video.paused = false;
        controlBtn.click();
        setTimeout(() => {
            expect(videoStatus.textContent).toBe('Video paused');
            expect(controlBtn.classList.contains('atlas-hero__video-control-play')).toBeTruthy();
            done();
        }, 100);
    });

    test('should update button correctly with play attributes', () => {
        videoPlayerController.updateButton('atlas-hero__video-control-play', 'Play video', 'Play');
        expect(controlBtn.classList.contains('atlas-hero__video-control-play')).toBeTruthy();
        expect(controlBtn.getAttribute('aria-label')).toBe('Play video');
        expect(controlBtn.querySelector('.atlas-hero__video-control-icon span').textContent).toBe('Play');
    });

    test('should update button correctly with pause attributes', () => {
        videoPlayerController.updateButton('atlas-hero__video-control-pause', 'Pause video', 'Pause');
        expect(controlBtn.classList.contains('atlas-hero__video-control-pause')).toBeTruthy();
        expect(controlBtn.getAttribute('aria-label')).toBe('Pause video');
        expect(controlBtn.querySelector('.atlas-hero__video-control-icon span').textContent).toBe('Pause');
    });

    test('should update aria-live element text when video is played', () => {
        video.paused = true;
        videoPlayerController.toggleVideoPlayPause();
        expect(videoStatus.textContent).toBe('Video playing');
    });

    test('should update aria-live element text when video is paused', () => {
        video.paused = false;
        videoPlayerController.toggleVideoPlayPause();
        setTimeout(() => {
            expect(videoStatus.textContent).toBe('Video paused');
            done();
        }, 100);
    });

});