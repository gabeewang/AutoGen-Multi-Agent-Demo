# AutoGen - AI Agent 協作範例

本專案是使用Microsoft的AutoGen(v0.7.5)開源AI Agent開發套件進行實作。建立兩位分別為不同角色AI Agent，透過協作完成使用者指定的目標任務。

## 專案重點

* 使用AutoGen建立多AI Agent，以進行協作
* 模擬不同角色分工，此專案模擬了「Researcher」與「Writer」兩角色
* 展示AI Agent間的自動對話與任務拆解過程

## 安裝說明

### 環境需求

* 需Python 3.10(含)以尚版本
* 建議創建並使用虛擬環境(venv)

### 安裝套件

安裝此專案所需的Python套件。輸入以下指令至terminal。

```
pip install -r requirements.txt
```

### 環境變數配置

建立 .env 文件，並將下方資料欄位與對應值新增至 .env 文件當中。
```
# OpenAI API Key
OPENAI_API_KEY=<your api key>
```

## 執行說明

進入cmd，並切換至對應專案目錄，並輸入以下指令。
```
python src/main.py
```

執行成功將會出現以下文字，就可輸入指派給AI Agents任務內容。
```
請輸入指派任務(輸入 'exit' 即離開): 
```

## Agent 架構說明

本專案包含兩個主要角色(AI Agent)

### 1. Researcher Agent

**負責任務理解與資料蒐集研究**
- 理解使用者的指派的任務需求
- 於網際網路上查找與整理相關資料
- 對相關資訊進行研究分析
- 提供整理後的相關內容草稿給Writer

### 2. Writer Agent

**負責內容生成與整理**
- 根據Researcher提供的資料進行寫作
- 將資料轉換為清晰、有條理的內容
- 優化語句流暢度與整體可讀性
- 將內容寫成Markdown格式
- 輸出最終結果，並儲存至使用者指定的檔案名稱與路徑

## 使用情境

使用者輸入指派任務。
```
請輸入指派任務(輸入 'exit' 即離開): 幫我整理Vue最新的測試版本Vue3.6的更新內容重點，並將內容經由整理，儲存至src資料夾中，檔名為vue3.6_.md
```

AI Agent們將會協助完成指派任務，並輸出作業過程。
![execution](images/execution_screenshot.png)

完成後，將輸出使用者指定的檔案名稱之文件至指定路徑當中。
![result](images/result.png)

## 結語

### 架構選擇的理由

在本專案當中，選擇使用Microsoft AutoGen建立多AI Agent協作，以完成使用者指派的任務。採用Researcher + Writer架構原因如下。

1. 任務分工明確<br>
透過創建不同角色(Research與Writer)進行任務分工，此架構可以透過為每個Agent設計專屬的System Prompt，使其專注於自己擅長的領域，讓AI Agent處理事情更加具有專業程度，例如Researcher專注資料蒐集與研究；Writer專注於內容專業生成與排版。
2. 模擬真實的團隊協作流程<br>
此專案的AI Agent的對話與協作的方式與人類團隊協作相似，方便使用者理解多AI Agent的工作與思考過程。
3. 擴展性佳<br>
未來若想加入更多功能(例如圖表生成)，可以透過新增新的Agent角色，而不影響現存的架構。


### 目前遇到問題

在專案開發的過程當中，遭遇了以下問題。

1. 參考資料來源可靠性問題<br>
此專案抓取資料來源主要來自搜尋引擎，AI Agent會透過爬蟲程式抓取搜尋結果排名較前的網站進行資料蒐集與研究。雖然這種方式可以快速獲得較熱門的資料，但由於搜尋結果受到搜尋引擎演算法的引響，資料的可靠性可能因此不穩定。
2. Writer提早與重複寫入文件<br>
在專案的執行過程中，發現Research Agent在進行初步資料搜尋，並未將資料深入研究時，僅輸出搜尋結果，Writer就會將該搜尋結果整理並輸出成Markdown格式，並儲存成文件檔案。這導致文件多次寫入，同時也造成不必要的token消耗。