import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { useQuery } from 'react-query';
import { Plus, List, Zap, Shield, Brain } from 'lucide-react';
import { contentAPI } from '../services/api';

const HomeContainer = styled.div`
  padding: 2rem 1rem;
`;

const HeroSection = styled.section`
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 1rem;
  margin-bottom: 3rem;
`;

const HeroTitle = styled.h1`
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
`;

const HeroSubtitle = styled.p`
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const HeroActions = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
`;

const FeaturesSection = styled.section`
  margin-bottom: 3rem;
`;

const SectionTitle = styled.h2`
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
  color: #1e293b;
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
`;

const FeatureCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
  }
`;

const FeatureIcon = styled.div`
  width: 4rem;
  height: 4rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: white;
`;

const FeatureTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1e293b;
`;

const FeatureDescription = styled.p`
  color: #6b7280;
  line-height: 1.6;
`;

const StatsSection = styled.section`
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
`;

const StatCard = styled.div`
  text-align: center;
`;

const StatNumber = styled.div`
  font-size: 2.5rem;
  font-weight: 800;
  color: #3b82f6;
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  color: #6b7280;
  font-weight: 500;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
`;

const ErrorMessage = styled.div`
  background: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
  margin: 1rem 0;
`;

function HomePage() {
  const { data: stats, isLoading, error } = useQuery('stats', contentAPI.getStats);

  return (
    <HomeContainer>
      <HeroSection>
        <HeroTitle>Phoenix Knowledge Engine</HeroTitle>
        <HeroSubtitle>
          AI-powered educational content generation that creates comprehensive learning materials
          through our innovative three-layer architecture.
        </HeroSubtitle>
        <HeroActions>
          <Link to="/generate" className="btn btn-primary">
            <Plus size={20} />
            Generate Content
          </Link>
          <Link to="/learning-objectives" className="btn btn-secondary">
            <List size={20} />
            View Content
          </Link>
        </HeroActions>
      </HeroSection>

      <FeaturesSection>
        <SectionTitle>How It Works</SectionTitle>
        <FeaturesGrid>
          <FeatureCard>
            <FeatureIcon>
              <Brain size={24} />
            </FeatureIcon>
            <FeatureTitle>Orchestrator AI</FeatureTitle>
            <FeatureDescription>
              Breaks down learning objectives into structured plans, creating a roadmap
              for comprehensive content generation.
            </FeatureDescription>
          </FeatureCard>

          <FeatureCard>
            <FeatureIcon>
              <Zap size={24} />
            </FeatureIcon>
            <FeatureTitle>Worker AI</FeatureTitle>
            <FeatureDescription>
              Generates specific content components like examples, facts, and concepts
              using specialized, focused prompts.
            </FeatureDescription>
          </FeatureCard>

          <FeatureCard>
            <FeatureIcon>
              <Shield size={24} />
            </FeatureIcon>
            <FeatureTitle>Quality Control</FeatureTitle>
            <FeatureDescription>
              Validates all content through automated checks including fact-checking,
              length validation, and schema verification.
            </FeatureDescription>
          </FeatureCard>
        </FeaturesGrid>
      </FeaturesSection>

      <StatsSection>
        <SectionTitle>System Statistics</SectionTitle>
        {isLoading && (
          <LoadingSpinner>
            <div className="spinner"></div>
          </LoadingSpinner>
        )}
        {error && (
          <ErrorMessage>
            Failed to load statistics. Please try again later.
          </ErrorMessage>
        )}
        {stats && (
          <StatsGrid>
            <StatCard>
              <StatNumber>{stats.learning_objectives.total}</StatNumber>
              <StatLabel>Learning Objectives</StatLabel>
            </StatCard>
            <StatCard>
              <StatNumber>{stats.knowledge_components.total}</StatNumber>
              <StatLabel>Knowledge Components</StatLabel>
            </StatCard>
            <StatCard>
              <StatNumber>{stats.comprehension_checks.total}</StatNumber>
              <StatLabel>Comprehension Checks</StatLabel>
            </StatCard>
            <StatCard>
              <StatNumber>{stats.learning_objectives.ready}</StatNumber>
              <StatLabel>Ready for Use</StatLabel>
            </StatCard>
          </StatsGrid>
        )}
      </StatsSection>
    </HomeContainer>
  );
}

export default HomePage;
