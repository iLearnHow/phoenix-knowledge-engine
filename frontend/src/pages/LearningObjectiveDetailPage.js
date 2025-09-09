import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { 
  ArrowLeft, CheckCircle, Clock, XCircle, AlertCircle, 
  BookOpen, Lightbulb, AlertTriangle, HelpCircle, 
  Shield, RefreshCw, Eye, EyeOff
} from 'lucide-react';
import { contentAPI } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
`;

const BackButton = styled(Link)`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  text-decoration: none;
  margin-bottom: 2rem;
  font-weight: 500;
  transition: color 0.2s;
  
  &:hover {
    color: #3b82f6;
  }
`;

const HeaderSection = styled.div`
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  padding: 2rem;
  margin-bottom: 2rem;
`;

const HeaderTop = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
`;

const TitleSection = styled.div`
  flex: 1;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
  line-height: 1.3;
`;

const CoreQuestion = styled.p`
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 1rem;
  line-height: 1.5;
`;

const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  
  &.status-draft {
    background-color: #fef3c7;
    color: #92400e;
  }
  
  &.status-generating {
    background-color: #dbeafe;
    color: #1e40af;
  }
  
  &.status-ready {
    background-color: #d1fae5;
    color: #065f46;
  }
  
  &.status-failed {
    background-color: #fee2e2;
    color: #991b1b;
  }
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 0.75rem;
  align-items: center;
`;

const Button = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  
  &.btn-primary {
    background: #3b82f6;
    color: white;
    
    &:hover:not(:disabled) {
      background: #2563eb;
    }
  }
  
  &.btn-secondary {
    background: #6b7280;
    color: white;
    
    &:hover:not(:disabled) {
      background: #4b5563;
    }
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const Summary = styled.div`
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid #3b82f6;
`;

const SummaryTitle = styled.h3`
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
`;

const SummaryText = styled.p`
  color: #6b7280;
  line-height: 1.6;
`;

const ContentSection = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  
  @media (min-width: 1024px) {
    grid-template-columns: 2fr 1fr;
  }
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Sidebar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Section = styled.div`
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const SectionHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
`;

const SectionTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const SectionContent = styled.div`
  padding: 1.5rem;
`;

const ComponentList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ComponentItem = styled.div`
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  
  &:hover {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const ComponentHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
`;

const ComponentType = styled.span`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  
  &.type-core_concept {
    background-color: #dbeafe;
    color: #1e40af;
  }
  
  &.type-fact {
    background-color: #d1fae5;
    color: #065f46;
  }
  
  &.type-example {
    background-color: #fef3c7;
    color: #92400e;
  }
  
  &.type-principle {
    background-color: #e0e7ff;
    color: #3730a3;
  }
  
  &.type-analogy {
    background-color: #fce7f3;
    color: #be185d;
  }
  
  &.type-warning {
    background-color: #fee2e2;
    color: #991b1b;
  }
`;

const ValidationStatus = styled.span`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  
  &.status-approved {
    background-color: #d1fae5;
    color: #065f46;
  }
  
  &.status-pending {
    background-color: #fef3c7;
    color: #92400e;
  }
  
  &.status-flagged {
    background-color: #fee2e2;
    color: #991b1b;
  }
`;

const ComponentContent = styled.div`
  color: #374151;
  line-height: 1.6;
`;

const QuestionItem = styled.div`
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
`;

const QuestionText = styled.p`
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 1rem;
`;

const OptionsList = styled.ul`
  list-style: none;
  margin-bottom: 1rem;
`;

const OptionItem = styled.li`
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 0.375rem;
  background: #f8fafc;
  
  &.correct {
    background: #d1fae5;
    border: 1px solid #10b981;
  }
`;

const Explanation = styled.div`
  padding: 0.75rem;
  background: #eff6ff;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #1e40af;
`;

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem;
`;

const ErrorContainer = styled.div`
  background: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
  margin: 2rem 0;
`;

const getTypeIcon = (type) => {
  switch (type) {
    case 'CORE_CONCEPT':
      return <BookOpen size={14} />;
    case 'FACT':
      return <Lightbulb size={14} />;
    case 'EXAMPLE':
      return <HelpCircle size={14} />;
    case 'PRINCIPLE':
      return <Shield size={14} />;
    case 'ANALOGY':
      return <Lightbulb size={14} />;
    case 'WARNING':
      return <AlertTriangle size={14} />;
    default:
      return <BookOpen size={14} />;
  }
};

const getStatusIcon = (status) => {
  switch (status) {
    case 'APPROVED':
      return <CheckCircle size={14} />;
    case 'PENDING':
      return <Clock size={14} />;
    case 'FLAGGED':
      return <AlertCircle size={14} />;
    default:
      return <XCircle size={14} />;
  }
};

function LearningObjectiveDetailPage() {
  const { id } = useParams();
  const [showAnswers, setShowAnswers] = useState(false);
  const queryClient = useQueryClient();
  
  const { data, isLoading, error } = useQuery(
    ['learning-objective', id],
    () => contentAPI.getLearningObjective(id)
  );
  
  const validateMutation = useMutation(
    () => contentAPI.validateContent({ learning_objective_id: id }),
    {
      onSuccess: () => {
        toast.success('Content validated successfully!');
        queryClient.invalidateQueries(['learning-objective', id]);
      },
      onError: (error) => {
        console.error('Validation error:', error);
        toast.error(error.response?.data?.message || 'Failed to validate content');
      }
    }
  );
  
  if (isLoading) {
    return (
      <PageContainer>
        <LoadingContainer>
          <div className="spinner"></div>
        </LoadingContainer>
      </PageContainer>
    );
  }
  
  if (error) {
    return (
      <PageContainer>
        <ErrorContainer>
          Failed to load learning objective. Please try again later.
        </ErrorContainer>
      </PageContainer>
    );
  }
  
  if (!data) {
    return (
      <PageContainer>
        <ErrorContainer>
          Learning objective not found.
        </ErrorContainer>
      </PageContainer>
    );
  }
  
  const { learning_objective, knowledge_components, comprehension_checks } = data;
  
  return (
    <PageContainer>
      <BackButton to="/learning-objectives">
        <ArrowLeft size={20} />
        Back to Learning Objectives
      </BackButton>
      
      <HeaderSection>
        <HeaderTop>
          <TitleSection>
            <Title>{learning_objective.title}</Title>
            <CoreQuestion>{learning_objective.core_question}</CoreQuestion>
          </TitleSection>
          <ActionButtons>
            <StatusBadge className={`status-${learning_objective.status.toLowerCase()}`}>
              {getStatusIcon(learning_objective.status)}
              {learning_objective.status.toLowerCase()}
            </StatusBadge>
            <Button
              className="btn-primary"
              onClick={() => validateMutation.mutate()}
              disabled={validateMutation.isLoading}
            >
              <RefreshCw size={16} />
              Validate
            </Button>
          </ActionButtons>
        </HeaderTop>
        
        <Summary>
          <SummaryTitle>Summary</SummaryTitle>
          <SummaryText>{learning_objective.summary}</SummaryText>
        </Summary>
      </HeaderSection>
      
      <ContentSection>
        <MainContent>
          <Section>
            <SectionHeader>
              <SectionTitle>
                <BookOpen size={20} />
                Knowledge Components ({knowledge_components.length})
              </SectionTitle>
            </SectionHeader>
            <SectionContent>
              <ComponentList>
                {knowledge_components.map((component) => (
                  <ComponentItem key={component.id}>
                    <ComponentHeader>
                      <ComponentType className={`type-${component.type.toLowerCase()}`}>
                        {getTypeIcon(component.type)}
                        {component.type.replace('_', ' ').toLowerCase()}
                      </ComponentType>
                      <ValidationStatus className={`status-${component.validation_status.toLowerCase()}`}>
                        {getStatusIcon(component.validation_status)}
                        {component.validation_status.toLowerCase()}
                      </ValidationStatus>
                    </ComponentHeader>
                    <ComponentContent>{component.content}</ComponentContent>
                  </ComponentItem>
                ))}
              </ComponentList>
            </SectionContent>
          </Section>
        </MainContent>
        
        <Sidebar>
          <Section>
            <SectionHeader>
              <SectionTitle>
                <HelpCircle size={20} />
                Assessment Questions ({comprehension_checks.length})
              </SectionTitle>
            </SectionHeader>
            <SectionContent>
              <div style={{ marginBottom: '1rem' }}>
                <Button
                  className="btn-secondary"
                  onClick={() => setShowAnswers(!showAnswers)}
                >
                  {showAnswers ? <EyeOff size={16} /> : <Eye size={16} />}
                  {showAnswers ? 'Hide' : 'Show'} Answers
                </Button>
              </div>
              {comprehension_checks.map((check) => (
                <QuestionItem key={check.id}>
                  <QuestionText>{check.question_text}</QuestionText>
                  <OptionsList>
                    {check.options.map((option, index) => (
                      <OptionItem
                        key={index}
                        className={showAnswers && index === check.correct_index ? 'correct' : ''}
                      >
                        {String.fromCharCode(65 + index)}. {option}
                      </OptionItem>
                    ))}
                  </OptionsList>
                  {showAnswers && (
                    <Explanation>
                      <strong>Explanation:</strong> {check.explanation}
                    </Explanation>
                  )}
                </QuestionItem>
              ))}
            </SectionContent>
          </Section>
        </Sidebar>
      </ContentSection>
    </PageContainer>
  );
}

export default LearningObjectiveDetailPage;
