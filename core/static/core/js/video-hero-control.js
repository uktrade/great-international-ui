class VideoPlayerController {
    constructor(video, controlBtn, options = {}) {
        this.video = video;
        this.controlBtn = controlBtn;
        this.playClass = options.playClass || 'atlas-hero__video-control-play';
        this.pauseClass = options.pauseClass || 'atlas-hero__video-control-pause';

        this.init();
    }

    init() {
        this.controlBtn.addEventListener('click', () => {
            this.toggleVideoPlayPause();
        });
    }

    toggleVideoPlayPause() {
        const isPlaying = !this.video.paused;

        if (isPlaying) {
            this.video.pause();
            this.updateButton(this.playClass, 'Play video', 'Play');
        } else {
            this.video.play();
            this.updateButton(this.pauseClass, 'Pause video', 'Pause');
        }
    }

    updateButton(btnClass, ariaLabel, buttonText) {
        this.controlBtn.classList.remove(this.playClass, this.pauseClass);
        this.controlBtn.classList.add(btnClass);
        this.controlBtn.setAttribute('aria-label', ariaLabel);
        this.controlBtn.querySelector('.atlas-hero__video-control-icon span').textContent = buttonText;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('js-atlas-video');
    const controlBtn = document.getElementById('js-video-control');

    if (video) {
        new VideoPlayerController(video, controlBtn);
    }
});
