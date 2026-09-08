import React from 'react';
import DocPage from '@theme-original/DocPage';
import Chatbot from '@site/src/components/Chatbot';

export default function DocPageWithChatbot(props) {
  return (
    <>
      <DocPage {...props} />
      <Chatbot />
    </>
  );
}