import React from 'react';
import { Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import LearningObjectivesPage from './pages/LearningObjectivesPage';
import LearningObjectiveDetailPage from './pages/LearningObjectiveDetailPage';
import GeneratePage from './pages/GeneratePage';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #f8fafc;
`;

const MainContent = styled.main`
  padding-top: 4rem; /* Account for fixed header */
`;

function App() {
  return (
    <AppContainer>
      <Header />
      <MainContent>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/generate" element={<GeneratePage />} />
          <Route path="/learning-objectives" element={<LearningObjectivesPage />} />
          <Route path="/learning-objectives/:id" element={<LearningObjectiveDetailPage />} />
        </Routes>
      </MainContent>
    </AppContainer>
  );
}

export default App;
