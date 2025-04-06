import { useState } from 'react'
import './App.css'

interface Question {
  id: keyof MovieRequest;
  text: string;
}

interface MovieRequest {
  favorite_movie_with_reason: string;
  release_year_preference: string;
  mood_preference: string;
}

interface MovieResponse {
  response: string;
}

function App() {
  const [currentView, setCurrentView] = useState<'questions' | 'movie'>('questions')
  const [movieRecommendation, setMovieRecommendation] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [answers, setAnswers] = useState<MovieRequest>({
    favorite_movie_with_reason: '',
    release_year_preference: '',
    mood_preference: ''
  })

  const questions: Question[] = [
    {
      id: 'favorite_movie_with_reason',
      text: "What's your favorite movie and why?"
    },
    {
      id: 'release_year_preference',
      text: 'Are you in the mood for something new or a classic?'
    },
    {
      id: 'mood_preference',
      text: 'Do you wanna have fun or do you want something serious?'
    }
  ]

  const handleAnswer = (questionId: keyof MovieRequest, answer: string) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }))
  }

  const handleSubmit = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(answers)
      })
      const data: MovieResponse = await response.json()
      setMovieRecommendation(data.response)
      setCurrentView('movie')
    } catch (error) {
      console.error('Error fetching recommendation:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setCurrentView('questions')
    setMovieRecommendation(null)
    setAnswers({
      favorite_movie_with_reason: '',
      release_year_preference: '',
      mood_preference: ''
    })
  }

  if (isLoading) {
    return (
      <div className="app-container">
        <div className="view-container loading-view">
          <div className="logo-container">
            <img src="/popcorn-logo.png" alt="PopChoice Logo" className="logo" />
            <h1 className="app-title">PopChoice</h1>
          </div>
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Finding your perfect movie...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      {currentView === 'questions' ? (
        <div className="view-container questions-view">
          <div className="logo-container">
            <img src="/popcorn-logo.png" alt="PopChoice Logo" className="logo" />
            <h1 className="app-title">PopChoice</h1>
          </div>
          
          <div className="questions-container">
            {questions.map((question) => (
              <div key={question.id} className="question-item">
                <p className="question-text">{question.text}</p>
                <input
                  type="text"
                  className="answer-input"
                  value={answers[question.id]}
                  onChange={(e) => handleAnswer(question.id, e.target.value)}
                  placeholder="Type your answer here..."
                />
              </div>
            ))}
          </div>

          <button 
            className="action-button"
            onClick={handleSubmit}
            disabled={Object.values(answers).some(answer => !answer)}
          >
            Let's Go
          </button>
        </div>
      ) : (
        <div className="view-container movie-view">
          <div className="logo-container">
            <img src="/popcorn-logo.png" alt="PopChoice Logo" className="logo" />
            <h1 className="app-title">PopChoice</h1>
          </div>

          {movieRecommendation && (
            <div className="movie-recommendation">
              <p className="movie-description">{movieRecommendation}</p>
            </div>
          )}

          <button className="action-button" onClick={handleReset}>
            Go Again
          </button>
        </div>
      )}
    </div>
  )
}

export default App
