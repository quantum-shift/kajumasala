import React, { useCallback, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import "antd/dist/reset.css"; 

import { Button, Dropdown, Input, Menu, Skeleton } from 'antd';
import TextArea from 'antd/es/input/TextArea';
import {Layout} from 'antd'
import { Content, Header } from 'antd/es/layout/layout';
import Sider from 'antd/es/layout/Sider';
import Icon, { PlusOutlined } from '@ant-design/icons';
import waveLogo from './wave.png'

const siderStyle: React.CSSProperties = {
  overflow: 'auto',
  height: '100vh',
  position: 'sticky',
  insetInlineStart: 0,
  top: 0,
  bottom: 0,
  scrollbarWidth: 'thin',
  scrollbarGutter: 'stable',
  backgroundColor: '#f0f0f0',
  padding: '20px'
};

const initialHistoryItems = [
  {
    title: 'Conversation AI eng demo'
  },
  {
    title: 'Conversation AI sales demo'
  },
  {
    title: 'Text2Speech marketing demo'
  },
]

const sendUserGoal = async (user_goal: string, language: string) => {
  try {
      const body = JSON.stringify({ 'user_query': user_goal, 'language': language });
      console.log('Request:', body);
      const response = await fetch('http://localhost:5001/generate', {
          method: 'POST',  // Use POST for sending data
          headers: {
              'Content-Type': 'application/json',
          },
          body: body,  // Payload
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();  // Parse JSON response
      console.log('Response:', data);
      return data;
  } catch (error) {
      console.error('Error:', error);
      return {
        final_video_path: '/user/naveenls/abc.mp4'
      }
  }
};

type PageState = {
  loading: boolean,
  inUse: boolean,
  pageUrl?: string
}

function App() {
  const [query, setQuery] = useState<string>()
  const [language, setLanguage] = useState<string>('en')

  const [historyItems, setHistoryItems] = useState(initialHistoryItems)
  const [pageState, setPageState] = useState<PageState>()

  const handleGenerate = useCallback(async () => {
    console.log("here" + query)
    if (!query) return

    setHistoryItems((historyItems) => [...historyItems, { title: query.slice(0, 20) }])
    setPageState({
      inUse: true,
      loading: true,
    })
    console.log("next" + query)
    const response = await sendUserGoal(query, language)
    console.log("How tf are we here")
    setPageState({
      inUse: true,
      loading: false,
      pageUrl: response['final_video_path']
    })
  }, [query])

  const handleNewDemo = useCallback(() => {
    setPageState(undefined)
  }, [])

  return (
      <Layout hasSider>
        <Sider style={siderStyle}>
          <div style={{
            fontSize: '1.25rem', 
            fontWeight: 500,
            paddingTop: 20,
            paddingBottom: 20
          }}>
              Demos
          </div>
          <div style={{paddingBottom: 20}}>
            <Button onClick={handleNewDemo} icon={<PlusOutlined />}>New Demo</Button>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: 16,}}>
            {historyItems.map((item, index) => 
              <div key={index}>{item.title}</div>
            )}
          </div>
        </Sider>
        <Layout>
          {
            pageState ? <Content style={{padding: '30px 50px'}}>
              <div style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
                <div style={{
                  fontSize: '1.25rem', 
                  fontWeight: 500,
                  padding: 20
                }}>
                    {query}
                </div>
                {
                  pageState.loading ? <Skeleton /> :
                  <div style={{
                    fontSize: '1.25rem', 
                    fontWeight: 500,
                    padding: 20
                  }}>
                    Check demo <a href={`file://${pageState.pageUrl}`} target="_blank" rel="noreferrer">here</a>🎉
                  </div>
                }
              </div>
            </Content> :
            <Content style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
              <div style={{
                width: '740px', 
                padding: '4px 12px', 
                border: '1px solid #ccc',
                borderRadius: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: 8
              }}>
                <TextArea 
                  rows={4} 
                  autoSize={{minRows: 3, maxRows: 3}} 
                  style={{background: 'transparent', border: 'none'}} 
                  placeholder="Ask any demo for product..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between'
                }}>
                  <Dropdown menu={{ 
                    onClick: (e) => setLanguage(e.key),
                    selectedKeys: language ? [language] : undefined, 
                    items: [
                    {
                      key: 'en',
                      label: 'English'
                    },
                    {
                      key: 'fr',
                      label: 'French'
                    },
                    {
                      key: 'de',
                      label: 'German'
                    },
                    {
                      key: 'nl',
                      label: 'Dutch'
                    }
                  ] }} trigger={['click']}>
                    <img src={waveLogo} alt="Icon" width={24} height={24} />
                  </Dropdown>
                  <Button 
                    type="primary" 
                    onClick={handleGenerate}
                  >
                    Generate
                  </Button>
                </div>
              </div>
            </Content>
          }
        </Layout>
      </Layout>
  );
}

export default App;
