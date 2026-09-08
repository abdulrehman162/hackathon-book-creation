import React from 'react';
import DocItemLayout from '@theme-original/DocItem/Layout';
import Chatbot from '@site/src/components/Chatbot';

export default function DocItemLayoutWithChatbot(props) {
  return (
    <>
      <DocItemLayout {...props} />
      <Chatbot />
    </>
  );
}