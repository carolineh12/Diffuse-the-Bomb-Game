#include <SFML/Audio.hpp>
#include <iostream>

class AudioPlayer {
private:
    sf::Music music;

public:
    AudioPlayer() {
        if (!music.openFromFile("ticking.ogg")) {
            std::cerr << "Failed to load audio file" << std::endl;
        }
    }

    void play() {
        music.play();
    }

    void pause() {
        music.pause();
    }

    void resume() {
        music.play();
    }

    void stop() {
        music.stop();
    }
};

int main() {
    AudioPlayer audioPlayer;
    audioPlayer.play();
    // Uncomment below lines to test pause, resume, and stop methods
    // audioPlayer.pause();
    // audioPlayer.resume();
    // audioPlayer.stop();

    // Keep the program running until a key is pressed
    std::cout << "Press any key to exit..." << std::endl;
    std::cin.get();
    
    return 0;
}
