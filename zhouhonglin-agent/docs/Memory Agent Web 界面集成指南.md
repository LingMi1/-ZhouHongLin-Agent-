# Memory Agent Web 界面集成指南

## 概述

本指南说明如何在 `src/zhouhonglin_agent/static/index.html` 中添加 Memory Agent 的前端界面。

## 需要添加的内容

### 1. 添加标签按钮

在第 739 行之后添加：

```html
<button class="tab" onclick="switchTab('memory')">🧠 Memory Management</button>
```

完整的标签栏应该是：

```html
<div class="tabs">
    <button class="tab active" onclick="switchTab('chat')">💬 智能对话</button>
    <button class="tab" onclick="switchTab('rag')">📚 RAG 问答</button>
    <button class="tab" onclick="switchTab('knowledge')">🗄️ 知识库管理</button>
    <button class="tab" onclick="switchTab('prompting')">🔗 Prompt Chaining</button>
    <button class="tab" onclick="switchTab('routing')">🎯 Routing Agent</button>
    <button class="tab" onclick="switchTab('parallelization')">🚀 Parallelization Agent</button>
    <button class="tab" onclick="switchTab('reflection')">💭 Reflection Agent</button>
    <button class="tab" onclick="switchTab('tooluse')">🔧 Tool Use Agent</button>
    <button class="tab" onclick="switchTab('planning')">📋 Planning Agent</button>
    <button class="tab" onclick="switchTab('multiagent')">👥 Multi-Agent Collaboration</button>
    <button class="tab" onclick="switchTab('memory')">🧠 Memory Management</button> <!-- 新增 -->
</div>
```

### 2. 添加内容区域

在其他标签页内容之后添加Memory标签页的内容区域。找到类似以下结构的位置：

```html
<!-- Multi-Agent Collaboration 内容 -->
<div id="multiagent-content" class="tab-content">
    ...
</div>

<!-- 在这里添加 Memory Management 内容 -->
```

### 3. Memory Management 界面代码

添加以下完整的Memory Management界面代码：

```html
<!-- Memory Management Agent 内容 -->
<div id="memory-content" class="tab-content">
    <div class="agent-header">
        <h2>🧠 Memory Management Agent</h2>
        <p class="agent-description">
            智能记忆管理系统 - 让AI拥有记忆能力，记住过去的对话、学习用户偏好、提供个性化服务
        </p>
    </div>

    <div class="memory-container">
        <!-- 左侧：记忆管理面板 -->
        <div class="memory-panel">
            <div class="panel-section">
                <h3>📝 存储新记忆</h3>
                <textarea id="memoryContent" placeholder="输入记忆内容..." rows="3"></textarea>
                
                <div class="memory-options">
                    <div class="option-group">
                        <label>记忆类型:</label>
                        <select id="memoryType">
                            <option value="semantic">📚 语义记忆 (事实知识)</option>
                            <option value="episodic">📖 情景记忆 (具体事件)</option>
                            <option value="long_term">💾 长期记忆 (用户偏好)</option>
                            <option value="short_term">⚡ 短期记忆 (临时信息)</option>
                            <option value="working">🔧 工作记忆 (任务相关)</option>
                            <option value="procedural">⚙️ 程序性记忆 (操作步骤)</option>
                        </select>
                    </div>
                    
                    <div class="option-group">
                        <label>重要性:</label>
                        <select id="memoryImportance">
                            <option value="5">⭐⭐⭐⭐⭐ 关键</option>
                            <option value="4">⭐⭐⭐⭐ 高</option>
                            <option value="3" selected>⭐⭐⭐ 中</option>
                            <option value="2">⭐⭐ 低</option>
                            <option value="1">⭐ 最低</option>
                        </select>
                    </div>
                    
                    <div class="option-group">
                        <label>标签 (逗号分隔):</label>
                        <input type="text" id="memoryTags" placeholder="例如: 用户偏好, Python, 编程">
                    </div>
                </div>
                
                <button onclick="storeMemory()" class="primary-btn">💾 存储记忆</button>
            </div>

            <div class="panel-section">
                <h3>🔍 检索记忆</h3>
                <input type="text" id="memoryQuery" placeholder="输入查询内容...">
                <div class="memory-filters">
                    <label>
                        <input type="checkbox" id="filterSemantic" checked> 语义
                    </label>
                    <label>
                        <input type="checkbox" id="filterEpisodic" checked> 情景
                    </label>
                    <label>
                        <input type="checkbox" id="filterLongTerm" checked> 长期
                    </label>
                </div>
                <button onclick="retrieveMemories()" class="primary-btn">🔍 搜索记忆</button>
            </div>

            <div class="panel-section">
                <h3>📊 记忆统计</h3>
                <div id="memoryStats" class="stats-display">
                    <p>加载中...</p>
                </div>
                <button onclick="loadMemoryStats()" class="secondary-btn">🔄 刷新统计</button>
            </div>
        </div>

        <!-- 右侧：对话和显示区域 -->
        <div class="memory-main">
            <div class="panel-section">
                <h3>💬 基于记忆的对话</h3>
                <div id="memoryMessages" class="messages-container"></div>
                <div class="input-area">
                    <textarea id="memoryChatInput" placeholder="输入消息... (AI会基于存储的记忆回答)" rows="2"></textarea>
                    <button onclick="sendMemoryChat()" class="primary-btn">发送</button>
                </div>
            </div>

            <div class="panel-section">
                <h3>📋 检索结果</h3>
                <div id="memoryResults" class="results-container">
                    <p class="placeholder">检索结果将显示在这里...</p>
                </div>
            </div>
        </div>
    </div>
</div>
```

### 4. 添加样式

在 `<style>` 标签中添加以下样式：

```css
/* Memory Management 样式 */
.memory-container {
    display: grid;
    grid-template-columns: 400px 1fr;
    gap: 20px;
    height: 100%;
}

.memory-panel {
    display: flex;
    flex-direction: column;
    gap: 15px;
    overflow-y: auto;
}

.memory-main {
    display: flex;
    flex-direction: column;
    gap: 15px;
    overflow-y: auto;
}

.panel-section {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.panel-section h3 {
    margin-bottom: 15px;
    color: #667eea;
    font-size: 16px;
}

.memory-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 15px 0;
}

.option-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.option-group label {
    font-size: 13px;
    color: #666;
    font-weight: 500;
}

.option-group select,
.option-group input {
    padding: 8px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    font-size: 14px;
}

.memory-filters {
    display: flex;
    gap: 15px;
    margin: 10px 0;
}

.memory-filters label {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 13px;
    cursor: pointer;
}

.stats-display {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    font-size: 13px;
    line-height: 1.6;
}

.stats-display p {
    margin: 5px 0;
}

.results-container {
    max-height: 400px;
    overflow-y: auto;
}

.memory-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 3px solid #667eea;
}

.memory-card-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 12px;
    color: #666;
}

.memory-card-content {
    font-size: 14px;
    color: #333;
    margin-bottom: 8px;
}

.memory-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.memory-tag {
    background: #667eea;
    color: white;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 11px;
}
```

### 5. 添加 JavaScript 函数

在 `<script>` 标签中添加以下函数：

```javascript
// Memory Management 相关函数
const MEMORY_SESSION_ID = 'default';

// 存储记忆
async function storeMemory() {
    const content = document.getElementById('memoryContent').value.trim();
    if (!content) {
        alert('请输入记忆内容');
        return;
    }
    
    const memoryType = document.getElementById('memoryType').value;
    const importance = parseInt(document.getElementById('memoryImportance').value);
    const tagsStr = document.getElementById('memoryTags').value;
    const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()) : [];
    
    try {
        const response = await fetch('/api/memory/store', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                content: content,
                memory_type: memoryType,
                importance: importance,
                tags: tags,
                session_id: MEMORY_SESSION_ID
            })
        });
        
        const data = await response.json();
        if (data.success) {
            alert('✅ 记忆已存储！');
            document.getElementById('memoryContent').value = '';
            document.getElementById('memoryTags').value = '';
            loadMemoryStats();
        }
    } catch (error) {
        console.error('存储记忆失败:', error);
        alert('存储记忆失败，请重试');
    }
}

// 检索记忆
async function retrieveMemories() {
    const query = document.getElementById('memoryQuery').value.trim();
    if (!query) {
        alert('请输入查询内容');
        return;
    }
    
    const memoryTypes = [];
    if (document.getElementById('filterSemantic').checked) memoryTypes.push('semantic');
    if (document.getElementById('filterEpisodic').checked) memoryTypes.push('episodic');
    if (document.getElementById('filterLongTerm').checked) memoryTypes.push('long_term');
    
    try {
        const response = await fetch('/api/memory/retrieve', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                query: query,
                memory_types: memoryTypes.length > 0 ? memoryTypes : null,
                top_k: 10,
                session_id: MEMORY_SESSION_ID
            })
        });
        
        const data = await response.json();
        displayMemoryResults(data.results);
    } catch (error) {
        console.error('检索记忆失败:', error);
        alert('检索记忆失败，请重试');
    }
}

// 显示检索结果
function displayMemoryResults(results) {
    const container = document.getElementById('memoryResults');
    if (!results || results.length === 0) {
        container.innerHTML = '<p class="placeholder">未找到相关记忆</p>';
        return;
    }
    
    container.innerHTML = results.map(result => `
        <div class="memory-card">
            <div class="memory-card-header">
                <span>${getMemoryTypeIcon(result.memory.memory_type)} ${result.memory.memory_type}</span>
                <span>相关性: ${(result.relevance_score * 100).toFixed(0)}%</span>
            </div>
            <div class="memory-card-content">${result.memory.content}</div>
            <div class="memory-card-tags">
                ${result.memory.tags.map(tag => `<span class="memory-tag">${tag}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// 获取记忆类型图标
function getMemoryTypeIcon(type) {
    const icons = {
        'semantic': '📚',
        'episodic': '📖',
        'long_term': '💾',
        'short_term': '⚡',
        'working': '🔧',
        'procedural': '⚙️'
    };
    return icons[type] || '💭';
}

// 加载记忆统计
async function loadMemoryStats() {
    try {
        const response = await fetch(`/api/memory/statistics/${MEMORY_SESSION_ID}`);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            const html = `
                <p><strong>📊 总记忆数:</strong> ${stats.total_memories}</p>
                <p><strong>📦 按类型分布:</strong></p>
                ${Object.entries(stats.by_type).map(([type, count]) => 
                    `<p style="margin-left:15px">${getMemoryTypeIcon(type)} ${type}: ${count}</p>`
                ).join('')}
                <p><strong>💾 存储大小:</strong> ${stats.storage_size_kb} KB</p>
            `;
            document.getElementById('memoryStats').innerHTML = html;
        }
    } catch (error) {
        console.error('加载统计失败:', error);
    }
}

// 基于记忆的对话
async function sendMemoryChat() {
    const input = document.getElementById('memoryChatInput');
    const userInput = input.value.trim();
    if (!userInput) return;
    
    // 添加用户消息
    addMemoryMessage('user', userInput);
    input.value = '';
    
    try {
        const response = await fetch('/api/memory/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_input: userInput,
                session_id: MEMORY_SESSION_ID
            })
        });
        
        const data = await response.json();
        if (data.success) {
            addMemoryMessage('assistant', data.response);
        }
    } catch (error) {
        console.error('对话失败:', error);
        addMemoryMessage('assistant', '抱歉，对话失败，请重试');
    }
}

// 添加消息到对话区域
function addMemoryMessage(role, content) {
    const container = document.getElementById('memoryMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    messageDiv.innerHTML = `
        <div class="message-content">${content}</div>
    `;
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    // 加载初始统计
    if (document.getElementById('memoryStats')) {
        loadMemoryStats();
    }
});
```

### 6. 修改 switchTab 函数

确保 `switchTab` 函数支持 'memory' 标签：

```javascript
function switchTab(tabName) {
    // 隐藏所有标签内容
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));
    
    // 移除所有标签的 active 类
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // 显示选中的标签内容
    const selectedContent = document.getElementById(tabName + '-content');
    if (selectedContent) {
        selectedContent.classList.add('active');
    }
    
    // 激活选中的标签
    event.target.classList.add('active');
    
    // Memory标签特殊处理
    if (tabName === 'memory') {
        loadMemoryStats();
    }
}
```

## 完成

完成以上步骤后，Memory Management Agent 的前端界面就集成完成了。启动服务器后，可以在 Web 界面中看到新的 "🧠 Memory Management" 标签页。

## 功能测试

1. 启动服务器：`python run_web.py`
2. 访问：`http://localhost:8001`
3. 点击 "🧠 Memory Management" 标签
4. 测试各项功能：
   - 存储记忆
   - 检索记忆
   - 基于记忆的对话
   - 查看统计信息

## 注意事项

- 确保后端API已正确配置
- 记忆会持久化存储在 `data/memories/` 目录
- 每个会话有独立的记忆存储
- 可以根据需要调整界面样式和布局

