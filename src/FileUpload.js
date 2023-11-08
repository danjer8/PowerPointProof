// FileUpload.js
import React, { useState } from 'react';

const FileUpload = () => {
    const [file, setFile] = useState(null); // Die ausgewählte Datei
    const [analysisResult, setAnalysisResult] = useState(null); // Die Antwort vom Server nach der Analyse

    // Event-Handler für die Dateiauswahl
    const handleFileChange = (event) => {
        setFile(event.target.files[0]); // Setze die ausgewählte Datei
        setAnalysisResult(null); // Setze das Analyseergebnis zurück, für den Fall dass bereits eines vorhanden war
    };

    // Event-Handler für das Absenden der Datei
    const handleFileUpload = async () => {
        if (!file) {
            alert('Bitte wählen Sie zuerst eine Datei aus.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP-Fehler: ${response.status}`);
            }

            const result = await response.json();
            setAnalysisResult(result); // Setze das Analyseergebnis mit der Antwort vom Server
        } catch (error) {
            console.error('Fehler beim Hochladen der Datei:', error);
            alert('Fehler beim Hochladen der Datei.');
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Hochladen</button>
            {analysisResult && (
                <div>
                    <h2>Analysedaten:</h2>
                    <p>Anzahl der Folien: {analysisResult.slide_count}</p>
                    <ul>
                        {analysisResult.feedback.map((feedback, index) => (
                            <li key={index}>{feedback}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
