import React, { useCallback, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import "antd/dist/reset.css";

import { Button, Dropdown, Input, Menu, Skeleton } from 'antd';
import TextArea from 'antd/es/input/TextArea';
import { Layout } from 'antd'
import { Content, Header } from 'antd/es/layout/layout';
import Sider from 'antd/es/layout/Sider';
import Icon, { PlusOutlined } from '@ant-design/icons';
import waveLogo from './wave.png'
import shareLogo from './share.svg'
import thumbsUpLogo from './thumbsUp.svg'
import thumbsDownLogo from './thumbsDown.svg'
import loomLogo from './loom.png'
import whatsAppLogo from './whatsapp.jpg'
import mailLogo from './email.png'
import salesLogo from './salesLogo.jpeg'

import type { CollapseProps, message } from 'antd';
import { Collapse } from 'antd';

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
  padding: '20px',
  width: 250,
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

const sendUserGoal = (user_goal: string, language: string, onMessage: any, onComplete: any, onError: any) => {
  return new Promise((resolve, reject) => {
    const eventSource = new EventSource(`http://localhost:5001/generate?user_query=${encodeURIComponent(user_goal)}&language=${encodeURIComponent(language)}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Streaming update:', data);

      if (onMessage) {
        onMessage(data);  // Callback for intermediate updates
      }

      if (data.status === 'success') {
        eventSource.close();
        resolve(data);
        if (onComplete) {
          onComplete(data);
        }
      }

      if (data.status === 'error') {
        eventSource.close();
        reject(data);
        if (onError) {
          onError(data);
        }
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE Error:', error);
      eventSource.close();
      reject(error);
      if (onError) {
        onError(error);
      }
    };
  });
};


type PageState = {
  loading: boolean,
  inUse: boolean,
  query?: string
  pageUrl?: string
  progressMessages?: any[];  // New field to track streaming updates
}

function App() {
  const [query, setQuery] = useState<string>()
  const [language, setLanguage] = useState<string>('en')

  const [historyItems, setHistoryItems] = useState(initialHistoryItems)
  const [pageState, setPageState] = useState<PageState>({
    inUse: false,
    loading: false,
    progressMessages: [],
  })

  const handleGenerate = useCallback(async () => {
    console.log("here" + query)
    if (!query) return

    setHistoryItems((historyItems) => [...historyItems, { title: query.slice(0, 20) }])
    setPageState({
      query,
      inUse: true,
      loading: true,
      progressMessages: [],
    })
    try {
      await sendUserGoal(
        query,
        language,
        (update: any) => {
          // Append new messages as they arrive
          setPageState((prevState) => ({
            ...prevState,
            progressMessages: [...(prevState.progressMessages || []), update.message],
          }));
        },
        (finalData: any) => {
          setPageState((prevState) => ({
            ...prevState,
            loading: false,
            pageUrl: finalData.final_video_path,
          }));
        },
        (error: any) => {
          console.error("Error:", error.message);
          setPageState((prevState) => ({
            ...prevState,
            loading: false,
            progressMessages: [...(prevState.progressMessages || []), "Error: " + error.message],
          }));
        }
      );
    } catch (error) {
      console.error("Unexpected Error:", error);
      setPageState((prevState) => ({
        ...prevState,
        loading: false,
        progressMessages: [...(prevState.progressMessages || []), "Unexpected error occurred."],
      }));
    }
    setQuery(undefined)
    setLanguage('en')
  }, [query])

  const handleNewDemo = useCallback(() => {
    setPageState({
      inUse: false,
      loading: false,
      progressMessages: [],
    })
  }, [])

  return (
    <Layout hasSider>
      <Sider style={siderStyle} width={250}>
        <div style={{
          fontSize: '1.25rem',
          fontWeight: 500,
          paddingTop: 20,
          paddingBottom: 20
        }}>
          Demos
        </div>
        <div style={{ paddingBottom: 20 }}>
          <Button onClick={handleNewDemo} icon={<PlusOutlined />}>New Demo</Button>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, }}>
          {historyItems.map((item, index) =>
            <div key={index} style={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            }}>{item.title}</div>
          )}
        </div>
      </Sider>
      <Layout>
        <Header style={{
          backgroundColor: 'transparent',
          fontSize: '18px',
          fontWeight: 400,
          color: '#727272'
        }}>
          <img src={salesLogo} alt="Icon" width={24} height={24} />&nbsp;
          Sales Demo Agent
        </Header>
        {
          pageState.inUse ? <Content style={{ padding: '30px 50px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{
                fontSize: '1.25rem',
                fontWeight: 500,
                padding: 20
              }}>
                {pageState.query}
              </div>
              <Collapse defaultActiveKey={['1']} ghost items={[
                {
                  key: '1',
                  label: 'Generating demo...',
                  children: <div style={{ color: '#727272', display: 'flex', flexDirection: 'column' }}>
                    {pageState.progressMessages?.map((message) => <div>{message}</div>)}
                  </div>
                }
              ]} />
              {pageState.pageUrl &&
                <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                  <div style={{
                    fontSize: '1.25rem',
                    fontWeight: 500,
                    paddingLeft: 20
                  }}>
                    Check demo <a href={`${pageState.pageUrl}`} target="_blank" rel="noreferrer">here</a>🎉
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'row', gap: 8, paddingLeft: 20 }}>
                    <img src={thumbsUpLogo} alt="Icon" width={16} height={16} />
                    <img src={thumbsDownLogo} alt="Icon" width={16} height={16} />
                    <Dropdown menu={{
                      onClick: (e) => setLanguage(e.key),
                      selectedKeys: language ? [language] : undefined,
                      items: [
                        {
                          key: 'whatasapp',
                          label: 'Whatasapp',
                          icon: <img src={whatsAppLogo} width={16} height={16} />
                        },
                        {
                          key: 'Mail',
                          label: 'Mail',
                          icon: <img src={mailLogo} width={16} height={16} />
                        },
                        {
                          key: 'loom',
                          label: 'Loom',
                          icon: <img src={loomLogo} width={16} height={16} />
                        }
                      ]
                    }} trigger={['click']}>
                      <img src={shareLogo} alt="Icon" width={16} height={16} />
                    </Dropdown>
                  </div>
                </div>
              }
            </div>
          </Content> :
            <Content style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
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
                  autoSize={{ minRows: 3, maxRows: 3 }}
                  style={{ background: 'transparent', border: 'none' }}
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
                    ]
                  }} trigger={['click']}>
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
