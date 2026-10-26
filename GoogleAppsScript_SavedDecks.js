/**
 * ============================================================================
 * UNIVERSE OF LEGENDS TCG - SAVED DECKS BACKEND
 * ============================================================================
 * Instructions to Deploy:
 * 1. Open your Google Sheet: "Universe of Legends - Saved Decks"
 *    https://docs.google.com/spreadsheets/d/1Z7mxql5ZswCbE927ZOIWmEbnadCA4fzIjLPyX3bqXFU/edit
 * 2. In the top menu, click Extensions -> Apps Script.
 * 3. Delete any default code in Code.gs, paste this entire script, and click Save (disk icon).
 * 4. In the top right, click "Deploy" -> "New deployment".
 * 5. Click the gear icon next to "Select type" and choose "Web app".
 * 6. Set:
 *    - Description: "Universe of Legends Decks API"
 *    - Execute as: "Me" (your Google account)
 *    - Who has access: "Anyone" (allows players to save/load decks without logging in)
 * 7. Click "Deploy", authorize permissions when prompted.
 * 8. Copy the "Web app URL" (ends in /exec) and paste it into the "⚙ Backend" modal in the game!
 * ============================================================================
 */

const SHEET_NAME = 'Sheet1';
const ADMIN_PASSCODE = 'UofLAdmin2026';

function doGet(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) {
      return createJsonResponse({ success: true, decks: [] });
    }
    
    const headers = data[0];
    const nameIdx = getColumnIndex(headers, ['Deck Name', 'Name', 'Deck']);
    const lockIdx = getColumnIndex(headers, ['LOCKED', 'Lock', 'IsLocked']);
    const barIdx = getColumnIndex(headers, ['Barriers', 'Barrier Deck']);
    const mainIdx = getColumnIndex(headers, ['Main Deck Count', 'Main Count', 'Main Deck']);
    const reacIdx = getColumnIndex(headers, ['Re/Action Count', 'Reaction Count', 'Re/Actions']);
    const dateIdx = getColumnIndex(headers, ['Last Updated', 'Date', 'Timestamp']);
    const jsonIdx = getColumnIndex(headers, ['Deck Data JSON', 'Deck Data', 'JSON']);
    
    const decks = [];
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const name = row[nameIdx] ? String(row[nameIdx]).trim() : '';
      if (!name) continue;
      
      const lockedVal = lockIdx !== -1 ? String(row[lockIdx]).trim().toUpperCase() : '';
      const isLocked = (lockedVal === 'X');
      const rawJson = jsonIdx !== -1 ? String(row[jsonIdx]).trim() : '';
      
      decks.push({
        deckName: name,
        isLocked: isLocked,
        barriers: barIdx !== -1 ? String(row[barIdx]) : '',
        mainCount: mainIdx !== -1 ? row[mainIdx] : 0,
        reactionCount: reacIdx !== -1 ? row[reacIdx] : 0,
        lastUpdated: dateIdx !== -1 ? String(row[dateIdx]) : '',
        deckDataJson: rawJson
      });
    }
    
    return createJsonResponse({ success: true, decks: decks });
  } catch (err) {
    return createJsonResponse({ success: false, error: err.toString() });
  }
}

function doPost(e) {
  try {
    let payload;
    if (e.postData && e.postData.contents) {
      payload = JSON.parse(e.postData.contents);
    } else if (e.parameter) {
      payload = e.parameter;
      if (typeof payload.deckData === 'string') {
        try { payload.deckData = JSON.parse(payload.deckData); } catch(ex){}
      }
    } else {
      payload = {};
    }
    
    const action = payload.action || 'saveDeck';
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
    const data = sheet.getDataRange().getValues();
    const headers = data[0];
    
    const nameIdx = getColumnIndex(headers, ['Deck Name', 'Name', 'Deck']);
    const lockIdx = getColumnIndex(headers, ['LOCKED', 'Lock', 'IsLocked']);
    const barIdx = getColumnIndex(headers, ['Barriers', 'Barrier Deck']);
    const mainIdx = getColumnIndex(headers, ['Main Deck Count', 'Main Count', 'Main Deck']);
    const reacIdx = getColumnIndex(headers, ['Re/Action Count', 'Reaction Count', 'Re/Actions']);
    const dateIdx = getColumnIndex(headers, ['Last Updated', 'Date', 'Timestamp']);
    const jsonIdx = getColumnIndex(headers, ['Deck Data JSON', 'Deck Data', 'JSON']);
    
    const isAdmin = payload.isAdmin === true || payload.passcode === ADMIN_PASSCODE;
    
    if (action === 'saveDeck' || action === 'updateDeck') {
      const deckName = (payload.deckName || '').trim();
      if (!deckName) {
        return createJsonResponse({ success: false, error: 'Deck name is required.' });
      }
      
      const deckDataJson = typeof payload.deckData === 'object' ? JSON.stringify(payload.deckData) : (payload.deckData || '');
      const barriers = payload.barriersSummary || '';
      const mainCount = payload.mainCount || 0;
      const reactionCount = payload.reactionCount || 0;
      const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || "GMT-4", "yyyy-MM-dd HH:mm:ss");
      const lockRequest = payload.isLocked === true || payload.isLocked === 'X' ? 'X' : '';
      
      // Search for existing deck by name
      let existingRow = -1;
      let isExistingLocked = false;
      
      for (let i = 1; i < data.length; i++) {
        if (String(data[i][nameIdx]).trim().toLowerCase() === deckName.toLowerCase()) {
          existingRow = i + 1; // 1-indexed for Sheet API
          const lVal = lockIdx !== -1 ? String(data[i][lockIdx]).trim().toUpperCase() : '';
          isExistingLocked = (lVal === 'X');
          break;
        }
      }
      
      if (existingRow !== -1) {
        // OVERRIDE CHECK: If locked and not admin, reject!
        if (isExistingLocked && !isAdmin) {
          return createJsonResponse({ 
            success: false, 
            isLocked: true,
            error: `Deck "${deckName}" is LOCKED with an 'X' in the Google Sheet and cannot be modified or overwritten.` 
          });
        }
        
        // Update existing row
        sheet.getRange(existingRow, nameIdx + 1).setValue(deckName);
        if (lockIdx !== -1 && isAdmin && payload.isLocked !== undefined) {
          sheet.getRange(existingRow, lockIdx + 1).setValue(lockRequest);
        }
        if (barIdx !== -1) sheet.getRange(existingRow, barIdx + 1).setValue(barriers);
        if (mainIdx !== -1) sheet.getRange(existingRow, mainIdx + 1).setValue(mainCount);
        if (reacIdx !== -1) sheet.getRange(existingRow, reacIdx + 1).setValue(reactionCount);
        if (dateIdx !== -1) sheet.getRange(existingRow, dateIdx + 1).setValue(timestamp);
        if (jsonIdx !== -1) sheet.getRange(existingRow, jsonIdx + 1).setValue(deckDataJson);
        
        return createJsonResponse({ 
          success: true, 
          action: 'updated',
          message: `Deck "${deckName}" updated successfully in Google Sheet!` 
        });
      } else {
        // Append new deck row
        const newRow = [];
        for (let col = 0; col < headers.length; col++) {
          if (col === nameIdx) newRow.push(deckName);
          else if (col === lockIdx) newRow.push(isAdmin ? lockRequest : '');
          else if (col === barIdx) newRow.push(barriers);
          else if (col === mainIdx) newRow.push(mainCount);
          else if (col === reacIdx) newRow.push(reactionCount);
          else if (col === dateIdx) newRow.push(timestamp);
          else if (col === jsonIdx) newRow.push(deckDataJson);
          else newRow.push('');
        }
        sheet.appendRow(newRow);
        
        return createJsonResponse({ 
          success: true, 
          action: 'created',
          message: `Deck "${deckName}" created and saved to Google Sheet!` 
        });
      }
    } else if (action === 'toggleLock') {
      const deckName = (payload.deckName || '').trim();
      if (!isAdmin) {
        return createJsonResponse({ success: false, error: 'Unauthorized: Only administrator can toggle deck locks.' });
      }
      
      let foundRow = -1;
      for (let i = 1; i < data.length; i++) {
        if (String(data[i][nameIdx]).trim().toLowerCase() === deckName.toLowerCase()) {
          foundRow = i + 1;
          break;
        }
      }
      
      if (foundRow === -1) {
        return createJsonResponse({ success: false, error: `Deck "${deckName}" not found.` });
      }
      
      const newLockState = (payload.lock === true || payload.lock === 'X') ? 'X' : '';
      sheet.getRange(foundRow, lockIdx + 1).setValue(newLockState);
      return createJsonResponse({ 
        success: true, 
        message: `Deck "${deckName}" lock status set to '${newLockState}'.` 
      });
    } else if (action === 'updateCard') {
      const cardName = (payload.cardName || '').trim();
      const origName = (payload.originalName || cardName).trim();
      if (!cardName) {
        return createJsonResponse({ success: false, error: 'Card name is required.' });
      }

      if (!isAdmin) {
        return createJsonResponse({ success: false, error: 'Unauthorized: Admin privileges required to edit cards.' });
      }

      const cardSheetId = payload.cardSheetId || '1yIp6ArxaQ-gGDVdY6EiR1RDuKzx_Np4i422sX0emmr0';
      let cardSs;
      try {
        cardSs = SpreadsheetApp.openById(cardSheetId);
      } catch (err) {
        return createJsonResponse({ success: false, error: 'Could not access Card List Sheet: ' + err.toString() });
      }

      const cardSheet = cardSs.getSheetByName('Sheet1') || cardSs.getSheets()[0];
      const cardData = cardSheet.getDataRange().getValues();
      const headers = cardData[0];

      const nameIdx = getColumnIndex(headers, ['Card Name', 'Name']);
      const typeIdx = getColumnIndex(headers, ['Card Type', 'Type']);
      const realmIdx = getColumnIndex(headers, ['Realm/Affinity', 'Realm', 'Affinity']);
      const colorIdx = getColumnIndex(headers, ['Card Color', 'Color']);
      const costIdx = getColumnIndex(headers, ['Energy Cost', 'Cost']);
      const atkIdx = getColumnIndex(headers, ['ATK']);
      const defIdx = getColumnIndex(headers, ['DEF', 'HP']);
      const textIdx = getColumnIndex(headers, ['Card Text & Abilities', 'Text', 'Abilities']);
      const kwIdx = getColumnIndex(headers, ['Keywords']);
      const imgIdx = getColumnIndex(headers, ['Image File Name', 'Image']);

      let foundRow = -1;
      for (let i = 1; i < cardData.length; i++) {
        if (String(cardData[i][nameIdx]).trim().toLowerCase() === origName.toLowerCase() ||
            String(cardData[i][nameIdx]).trim().toLowerCase() === cardName.toLowerCase()) {
          foundRow = i + 1;
          break;
        }
      }

      if (foundRow !== -1) {
        if (nameIdx !== -1) cardSheet.getRange(foundRow, nameIdx + 1).setValue(cardName);
        if (typeIdx !== -1 && payload.type !== undefined) cardSheet.getRange(foundRow, typeIdx + 1).setValue(payload.type);
        if (realmIdx !== -1 && payload.realm !== undefined) cardSheet.getRange(foundRow, realmIdx + 1).setValue(payload.realm);
        if (colorIdx !== -1 && payload.color !== undefined) cardSheet.getRange(foundRow, colorIdx + 1).setValue(payload.color);
        if (costIdx !== -1 && payload.cost !== undefined) cardSheet.getRange(foundRow, costIdx + 1).setValue(payload.cost);
        if (atkIdx !== -1 && payload.atk !== undefined) cardSheet.getRange(foundRow, atkIdx + 1).setValue(payload.atk);
        if (defIdx !== -1 && payload.hp !== undefined) cardSheet.getRange(foundRow, defIdx + 1).setValue(payload.hp);
        if (textIdx !== -1 && payload.text !== undefined) cardSheet.getRange(foundRow, textIdx + 1).setValue(payload.text);
        if (kwIdx !== -1 && payload.keywords !== undefined) cardSheet.getRange(foundRow, kwIdx + 1).setValue(payload.keywords);
        if (imgIdx !== -1 && payload.image !== undefined) cardSheet.getRange(foundRow, imgIdx + 1).setValue(payload.image);

        return createJsonResponse({ 
          success: true, 
          action: 'updated',
          message: `Card "${cardName}" updated successfully in Google Sheet!` 
        });
      } else {
        const newRow = [];
        for (let col = 0; col < headers.length; col++) {
          if (col === nameIdx) newRow.push(cardName);
          else if (col === typeIdx) newRow.push(payload.type || '');
          else if (col === realmIdx) newRow.push(payload.realm || '');
          else if (col === colorIdx) newRow.push(payload.color || '');
          else if (col === costIdx) newRow.push(payload.cost || '');
          else if (col === atkIdx) newRow.push(payload.atk || '');
          else if (col === defIdx) newRow.push(payload.hp || '');
          else if (col === textIdx) newRow.push(payload.text || '');
          else if (col === kwIdx) newRow.push(payload.keywords || '');
          else if (col === imgIdx) newRow.push(payload.image || '');
          else newRow.push('');
        }
        cardSheet.appendRow(newRow);

        return createJsonResponse({ 
          success: true, 
          action: 'created',
          message: `Card "${cardName}" created and added to Google Sheet!` 
        });
      }
    }
    
    return createJsonResponse({ success: false, error: 'Unknown action specified.' });
  } catch (err) {
    return createJsonResponse({ success: false, error: err.toString() });
  }
}

function getColumnIndex(headers, possibleNames) {
  for (let i = 0; i < headers.length; i++) {
    const h = String(headers[i]).trim().toLowerCase();
    for (let j = 0; j < possibleNames.length; j++) {
      if (h === possibleNames[j].toLowerCase()) return i;
    }
  }
  return -1;
}

function createJsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
