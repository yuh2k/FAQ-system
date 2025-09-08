import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';

// Mock axios for testing
jest.mock('axios');

// Mock antd message to avoid warnings
jest.mock('antd', () => {
  const antd = jest.requireActual('antd');
  return {
    ...antd,
    message: {
      error: jest.fn(),
      success: jest.fn(),
      info: jest.fn(),
      warning: jest.fn(),
    },
  };
});

describe('App Component', () => {
  test('renders welcome modal on first load', () => {
    render(<App />);
    
    expect(screen.getByText('Welcome to FAQ System')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your email address')).toBeInTheDocument();
    expect(screen.getByText('Start Chat')).toBeInTheDocument();
  });

  test('validates email input', async () => {
    render(<App />);
    
    const emailInput = screen.getByPlaceholderText('Enter your email address');
    const startButton = screen.getByText('Start Chat');
    
    // Test empty email
    fireEvent.click(startButton);
    // Should not proceed without email
    expect(screen.getByText('Welcome to FAQ System')).toBeInTheDocument();
    
    // Test invalid email
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.click(startButton);
    expect(screen.getByText('Welcome to FAQ System')).toBeInTheDocument();
    
    // Test valid email
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.queryByText('Welcome to FAQ System')).not.toBeInTheDocument();
    });
  });

  test('renders main navigation after email setup', async () => {
    render(<App />);
    
    const emailInput = screen.getByPlaceholderText('Enter your email address');
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.click(screen.getByText('Start Chat'));
    
    await waitFor(() => {
      expect(screen.getByText('Chat Support')).toBeInTheDocument();
      expect(screen.getByText('Support Tickets')).toBeInTheDocument();
      expect(screen.getByText('Knowledge Base')).toBeInTheDocument();
    });
  });

  test('switches between navigation items', async () => {
    render(<App />);
    
    // Setup email first
    const emailInput = screen.getByPlaceholderText('Enter your email address');
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.click(screen.getByText('Start Chat'));
    
    await waitFor(() => {
      // Should start with Chat Support
      expect(screen.getByText('Chat Support')).toBeInTheDocument();
    });
    
    // Click on Support Tickets
    fireEvent.click(screen.getByText('Support Tickets'));
    await waitFor(() => {
      expect(screen.getByText('Support Tickets')).toBeInTheDocument();
    });
    
    // Click on Knowledge Base
    fireEvent.click(screen.getByText('Knowledge Base'));
    await waitFor(() => {
      expect(screen.getByText('Knowledge Base')).toBeInTheDocument();
    });
  });

  test('displays user contact in header', async () => {
    render(<App />);
    
    const testEmail = 'test@example.com';
    const emailInput = screen.getByPlaceholderText('Enter your email address');
    fireEvent.change(emailInput, { target: { value: testEmail } });
    fireEvent.click(screen.getByText('Start Chat'));
    
    await waitFor(() => {
      expect(screen.getByText(testEmail)).toBeInTheDocument();
    });
  });
});

describe('Email Validation', () => {
  test('accepts valid email formats', () => {
    const validEmails = [
      'test@example.com',
      'user.name@domain.co.uk',
      'user+tag@example.org',
    ];
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    validEmails.forEach(email => {
      expect(emailRegex.test(email)).toBe(true);
    });
  });

  test('rejects invalid email formats', () => {
    const invalidEmails = [
      'invalid-email',
      '@example.com',
      'user@',
      'user@domain',
      'user space@example.com',
    ];
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    invalidEmails.forEach(email => {
      expect(emailRegex.test(email)).toBe(false);
    });
  });
});