import React, { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { Send, Loader } from 'lucide-react';
import { contentAPI } from '../services/api';

const GenerateContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
`;

const PageTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
  color: #1e293b;
`;

const FormCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const FormTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1e293b;
`;

const FormDescription = styled.p`
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.6;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: 500;
  color: #374151;
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

// TextArea component removed as it's not used in this component

const Select = styled.select`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
  transition: border-color 0.2s, box-shadow 0.2s;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const Button = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover:not(:disabled) {
    background: #2563eb;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const LoadingButton = styled(Button)`
  background: #6b7280;
`;

const ExamplesSection = styled.div`
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
`;

const ExamplesTitle = styled.h3`
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #374151;
`;

const ExamplesList = styled.ul`
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
`;

const ExampleItem = styled.li`
  padding: 0.5rem;
  background: white;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #6b7280;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background: #e5e7eb;
  }
`;

const exampleTopics = [
  'The Pythagorean Theorem',
  'Photosynthesis Process',
  'World War II Causes',
  'Newton\'s Laws of Motion',
  'The Water Cycle',
  'Democracy vs. Autocracy',
  'The Human Digestive System',
  'Climate Change Effects',
  'The Renaissance Period',
  'Basic Algebra Concepts'
];

function GeneratePage() {
  const [formData, setFormData] = useState({
    topic: '',
    priority: 0
  });
  
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  const generateMutation = useMutation(contentAPI.generateContent, {
    onSuccess: (data) => {
      toast.success('Content generated successfully!');
      queryClient.invalidateQueries('learning-objectives');
      queryClient.invalidateQueries('stats');
      navigate(`/learning-objectives/${data.learning_objective.id}`);
    },
    onError: (error) => {
      console.error('Generation error:', error);
      toast.error(error.response?.data?.message || 'Failed to generate content');
    }
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.topic.trim()) {
      toast.error('Please enter a topic');
      return;
    }
    generateMutation.mutate(formData);
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleExampleClick = (topic) => {
    setFormData(prev => ({
      ...prev,
      topic
    }));
  };
  
  return (
    <GenerateContainer>
      <PageTitle>Generate Educational Content</PageTitle>
      
      <FormCard>
        <FormTitle>Create New Learning Objective</FormTitle>
        <FormDescription>
          Enter a topic and our AI will generate a comprehensive learning objective with
          knowledge components, examples, and assessment questions.
        </FormDescription>
        
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="topic">Learning Topic *</Label>
            <Input
              type="text"
              id="topic"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              placeholder="e.g., The Pythagorean Theorem"
              required
            />
          </FormGroup>
          
          <FormGroup>
            <Label htmlFor="priority">Priority Level</Label>
            <Select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleInputChange}
            >
              <option value={0}>Normal</option>
              <option value={1}>High</option>
              <option value={2}>Urgent</option>
            </Select>
          </FormGroup>
          
          {generateMutation.isLoading ? (
            <LoadingButton disabled>
              <Loader size={20} className="spinner" />
              Generating Content...
            </LoadingButton>
          ) : (
            <Button type="submit">
              <Send size={20} />
              Generate Content
            </Button>
          )}
        </Form>
        
        <ExamplesSection>
          <ExamplesTitle>Example Topics</ExamplesTitle>
          <ExamplesList>
            {exampleTopics.map((topic, index) => (
              <ExampleItem
                key={index}
                onClick={() => handleExampleClick(topic)}
              >
                {topic}
              </ExampleItem>
            ))}
          </ExamplesList>
        </ExamplesSection>
      </FormCard>
    </GenerateContainer>
  );
}

export default GeneratePage;
