import azure.cognitiveservices.speech as speechsdk

# Replace with your Azure Speech Service credentials
speech_key = "33CdPfLtJO97wuA8D4g0HVgTLQY2KoUd0LsPWLljh9VAI0AvOKhKJQQJ99ALACGhslBXJ3w3AAAYACOGjosA"
service_region = "centralindia"

def continuous_language_recognition(file_path):
    # Language auto-detection configuration
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["en-US", "fr-FR", "ta-IN"]
    )

    # Speech configuration and audio input
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(filename=file_path)

    # Create a recognizer
    recognizer = speechsdk.SourceLanguageRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
        auto_detect_source_language_config=auto_detect_source_language_config
    )

    # Define event handlers
    def recognized_handler(evt):
        detected_language = evt.result.properties[
            speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult
        ]
        print(f"Detected Language: {detected_language}")
        print(f"Recognized Text: {evt.result.text}")

    def canceled_handler(evt):
        print(f"Recognition canceled: {evt.reason}")

    # Attach event handlers
    recognizer.recognized.connect(recognized_handler)
    recognizer.canceled.connect(canceled_handler)

    # Start continuous recognition
    print("Starting continuous recognition...")
    recognizer.start_continuous_recognition()

    # Keep the script running until the audio is fully processed
    input("Press Enter to stop recognition...\n")
 
    # Stop recognition
    recognizer.stop_continuous_recognition()
    print("Recognition stopped.")

if __name__ == "__main__":
    audio_file = "audio/ta.wav"  # Example: "long_audio.wav"
    continuous_language_recognition(audio_file)