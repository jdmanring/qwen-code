import { describe, it, expect, vi } from 'vitest';
import { QwenAgent } from './qwen-agent';
import { ClientSideConnection } from '@agentclientprotocol/sdk';

const mockRequest = vi.fn();
const mockNotify = vi.fn();
const mockClose = vi.fn();

vi.mock('@agentclientprotocol/sdk', () => ({
  ClientSideConnection: vi.fn().mockImplementation(() => ({
    request: mockRequest,
    notify: mockNotify,
    close: mockClose,
    signal: { aborted: false },
    closed: Promise.resolve(),
  })),
  PROTOCOL_VERSION: '1.0.0',
  ndJsonStream: vi.fn(),
}));

describe('QwenAgent', () => {
  it('should call session/set_model when setModel is called', async () => {
    const config = {
      workspace: { rootPath: '/tmp/workspace', id: 'test-ws' },
      session: { id: 'test-session' },
      model: 'gpt-4o',
      provider: 'qwen',
    };
    
    const agent = new QwenAgent(config as any);
    (agent as any).availableModelIds = new Set(['gpt-4o']);
    (agent as any).qwenSessionId = 'test-sdk-session';
    
    // Mock the lease and connection to bypass "process not running" error
    const mockConnection = new ClientSideConnection();
    (agent as any).acpLease = {
      isActive: () => true,
    };
    (agent as any).connection = mockConnection;
    
    agent.setModel('gpt-4o');
    await new Promise(resolve => setTimeout(resolve, 50));
    
    expect(mockRequest).toHaveBeenCalledWith(
      'session/set_model',
      expect.objectContaining({
        modelId: 'gpt-4o',
      }),
    );
  });
});
