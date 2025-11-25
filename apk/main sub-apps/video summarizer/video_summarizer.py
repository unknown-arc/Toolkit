import os
import tempfile
import time
import logging
from typing import Optional, Dict
import moviepy.editor as mp
from pydub import AudioSegment
import speech_recognition as sr
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk
from openai import OpenAI

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

logger = logging.getLogger(__name__)

class VideoSummarizer:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.recognizer = sr.Recognizer()
        self.openai_client = None
        
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        elif os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def extract_audio(self, video_path: str) -> str:
        """Extract audio from video file"""
        try:
            logger.info(f"Extracting audio from: {video_path}")
            video = mp.VideoFileClip(video_path)
            audio_path = tempfile.mktemp(suffix=".wav")
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            return audio_path
        except Exception as e:
            raise Exception(f"Audio extraction failed: {str(e)}")
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using speech recognition"""
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Convert to WAV if needed using pydub
            if audio_path.endswith('.mp3'):
                audio = AudioSegment.from_mp3(audio_path)
                wav_path = tempfile.mktemp(suffix=".wav")
                audio.export(wav_path, format="wav")
                audio_path = wav_path
            
            # Use speech recognition
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for the audio data
                logger.info("Listening to audio...")
                audio_data = self.recognizer.record(source)
                
                # Recognize speech
                logger.info("Recognizing speech...")
                text = self.recognizer.recognize_google(audio_data)
                
                return text
                
        except sr.UnknownValueError:
            raise Exception("Speech recognition could not understand the audio. The video might not contain clear speech.")
        except sr.RequestError as e:
            raise Exception(f"Speech recognition service error: {str(e)}")
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def summarize_with_ai(self, text: str, sentences_count: int = 3) -> str:
        """Summarize text using OpenAI GPT"""
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
        
        try:
            logger.info("Generating AI summary...")
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries of video content."},
                    {"role": "user", "content": f"Please summarize the following video transcript in {sentences_count} clear, concise sentences:\n\n{text}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"AI summarization failed: {str(e)}")
    
    def summarize_with_extractive(self, text: str, sentences_count: int = 3) -> str:
        """Summarize text using extractive summarization"""
        try:
            logger.info("Generating extractive summary...")
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            
            summary_sentences = summarizer(parser.document, sentences_count)
            summary = " ".join(str(sentence) for sentence in summary_sentences)
            return summary
        except Exception as e:
            raise Exception(f"Extractive summarization failed: {str(e)}")
    
    def get_video_duration(self, video_path: str) -> str:
        """Get video duration in readable format"""
        try:
            video = mp.VideoFileClip(video_path)
            duration_seconds = video.duration
            video.close()
            
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            return f"{minutes}m {seconds}s"
        except:
            return "Unknown"
    
    def summarize_video(self, 
                       video_path: str,
                       summary_length: int = 3,
                       use_ai: bool = True) -> Dict:
        """
        Main method to summarize video from file
        
        Args:
            video_path: Path to local video file
            summary_length: Number of sentences in summary
            use_ai: Whether to use AI (OpenAI) or extractive summarization
        
        Returns:
            Dictionary containing summary and metadata
        """
        start_time = time.time()
        temp_files = []
        
        try:
            if not os.path.exists(video_path):
                raise Exception("Video file not found")
            
            # Step 1: Extract audio
            logger.info("Step 1: Extracting audio from video...")
            audio_path = self.extract_audio(video_path)
            temp_files.append(audio_path)
            
            # Step 2: Transcribe audio
            logger.info("Step 2: Transcribing audio to text...")
            transcribed_text = self.transcribe_audio(audio_path)
            
            if not transcribed_text or len(transcribed_text.strip()) < 10:
                raise Exception("Transcription resulted in empty or very short text. The video might not contain clear speech.")
            
            # Step 3: Generate summary
            logger.info("Step 3: Generating summary...")
            if use_ai and self.openai_client:
                summary = self.summarize_with_ai(transcribed_text, summary_length)
            else:
                summary = self.summarize_with_extractive(transcribed_text, summary_length)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Get video duration
            duration = self.get_video_duration(video_path)
            
            logger.info("Video processing completed successfully!")
            
            return {
                "summary": summary,
                "transcript": transcribed_text,
                "duration": duration,
                "processing_time": round(processing_time, 2),
                "word_count": len(summary.split())
            }
            
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            raise
        finally:
            # Cleanup temporary files
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    logger.warning(f"Could not delete temp file {temp_file}: {e}")