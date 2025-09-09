import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import styled from 'styled-components';
import { Search, Filter, Eye, CheckCircle, Clock, XCircle, AlertCircle } from 'lucide-react';
import { contentAPI } from '../services/api';

const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
`;

const PageHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const PageTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
`;

const ControlsContainer = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
`;

const SearchInput = styled.input`
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  min-width: 200px;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const FilterSelect = styled.select`
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background: white;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
  }
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
`;

const LearningObjectiveCard = styled.div`
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
  }
`;

const CardHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
`;

const CardTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
  line-height: 1.4;
`;

const CardQuestion = styled.p`
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  line-height: 1.5;
`;

const CardMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
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

const DateText = styled.span`
  color: #9ca3af;
  font-size: 0.75rem;
`;

const CardBody = styled.div`
  padding: 1.5rem;
`;

const CardSummary = styled.p`
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;

const CardStats = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
`;

const StatItem = styled.span`
  display: flex;
  align-items: center;
  gap: 0.25rem;
`;

const CardActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ViewButton = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s;
  
  &:hover {
    background: #2563eb;
  }
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

const EmptyContainer = styled.div`
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
`;

const EmptyTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
`;

const EmptyDescription = styled.p`
  margin-bottom: 2rem;
`;

const CreateButton = styled(Link)`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s;
  
  &:hover {
    background: #2563eb;
  }
`;

function LearningObjectivesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  
  const { data, isLoading, error } = useQuery(
    ['learning-objectives', { search: searchQuery, status: statusFilter }],
    () => contentAPI.getLearningObjectives({
      search: searchQuery || undefined,
      status: statusFilter || undefined
    }),
    {
      keepPreviousData: true
    }
  );
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'READY':
        return <CheckCircle size={14} />;
      case 'GENERATING':
        return <Clock size={14} />;
      case 'FAILED':
        return <XCircle size={14} />;
      default:
        return <AlertCircle size={14} />;
    }
  };
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };
  
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
          Failed to load learning objectives. Please try again later.
        </ErrorContainer>
      </PageContainer>
    );
  }
  
  return (
    <PageContainer>
      <PageHeader>
        <PageTitle>Learning Objectives</PageTitle>
        <ControlsContainer>
          <div style={{ position: 'relative' }}>
            <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#9ca3af' }} />
            <SearchInput
              type="text"
              placeholder="Search topics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ paddingLeft: '2.5rem' }}
            />
          </div>
          <div style={{ position: 'relative' }}>
            <Filter size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#9ca3af' }} />
            <FilterSelect
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              style={{ paddingLeft: '2.5rem' }}
            >
              <option value="">All Status</option>
              <option value="DRAFT">Draft</option>
              <option value="GENERATING">Generating</option>
              <option value="READY">Ready</option>
              <option value="FAILED">Failed</option>
            </FilterSelect>
          </div>
        </ControlsContainer>
      </PageHeader>
      
      {data?.results?.length === 0 ? (
        <EmptyContainer>
          <EmptyTitle>No Learning Objectives Found</EmptyTitle>
          <EmptyDescription>
            {searchQuery || statusFilter
              ? 'No learning objectives match your current filters.'
              : 'Get started by creating your first learning objective.'}
          </EmptyDescription>
          <CreateButton to="/generate">
            Create Learning Objective
          </CreateButton>
        </EmptyContainer>
      ) : (
        <ContentGrid>
          {data?.results?.map((objective) => (
            <LearningObjectiveCard key={objective.id}>
              <CardHeader>
                <CardTitle>{objective.title}</CardTitle>
                <CardQuestion>{objective.core_question}</CardQuestion>
                <CardMeta>
                  <StatusBadge className={`status-${objective.status.toLowerCase()}`}>
                    {getStatusIcon(objective.status)}
                    {objective.status.toLowerCase()}
                  </StatusBadge>
                  <DateText>{formatDate(objective.created_at)}</DateText>
                </CardMeta>
              </CardHeader>
              <CardBody>
                <CardSummary>{objective.summary}</CardSummary>
                <CardStats>
                  <StatItem>
                    <span>{objective.knowledge_components_count} components</span>
                  </StatItem>
                  <StatItem>
                    <span>{objective.comprehension_checks_count} questions</span>
                  </StatItem>
                </CardStats>
                <CardActions>
                  <ViewButton to={`/learning-objectives/${objective.id}`}>
                    <Eye size={16} />
                    View Details
                  </ViewButton>
                </CardActions>
              </CardBody>
            </LearningObjectiveCard>
          ))}
        </ContentGrid>
      )}
    </PageContainer>
  );
}

export default LearningObjectivesPage;
