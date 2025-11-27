# 📊 Airtable Integration Setup

## 1. Create Airtable Base

1. Go to https://airtable.com
2. Create a new base called "AI Influencer Videos"
3. Create a table called "AI_Influencer_Videos"

## 2. Table Structure

Create these fields in your Airtable table:

| Field Name | Type | Description |
|------------|------|-------------|
| Job ID | Single line text | Unique job identifier |
| Type | Single select | Character, Video, or Voiceover |
| Description | Long text | Character/product description |
| Prompt | Long text | Video generation prompt |
| Product Description | Long text | Product details |
| Script | Long text | Voiceover script |
| Language | Single line text | Language code |
| Aspect Ratio | Single line text | Video aspect ratio |
| Duration (seconds) | Number | Video duration |
| Status | Single select | Pending, Processing, Completed, Failed |
| Created At | Date | Creation timestamp |
| Updated At | Date | Last update timestamp |
| Reference Images | Attachment | Character reference images |
| Files | Attachment | Generated videos/audio |
| Metadata | Long text | Additional metadata (JSON) |
| Error | Long text | Error message if failed |

## 3. Get API Credentials

### Get API Key
1. Go to https://airtable.com/create/tokens
2. Click "Create new token"
3. Name it "AI Influencer API"
4. Add these scopes:
   - `data.records:read`
   - `data.records:write`
5. Add access to your base
6. Click "Create token"
7. Copy the token (starts with `pat...`)

### Get Base ID
1. Go to https://airtable.com/api
2. Select your base
3. The Base ID is in the URL: `https://airtable.com/[BASE_ID]/api/docs`
4. Or find it in the API documentation

## 4. Configure .env File

Add to your `.env` file:

```bash
# Airtable Configuration
AIRTABLE_API_KEY=patXXXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=AI_Influencer_Videos
```

## 5. Install Dependencies

```bash
pip install pyairtable
```

## 6. Test Connection

```bash
python src/airtable_integration.py
```

You should see:
```
✅ Airtable connection successful!
📋 Recent records: 0
```

## 7. Usage

The API will automatically save to Airtable when configured.

### View Records

Go to your Airtable base to see:
- All generated characters
- All generated videos
- All voiceovers
- Timestamps and metadata
- Attached files (images/videos)

## 8. Optional: Cloud Storage

For production, upload files to cloud storage first:

```bash
# Add to .env
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=your-bucket
```

Then update `airtable_integration.py` to upload to S3 and use public URLs.

## Troubleshooting

**Error: "AIRTABLE_API_KEY not found"**
- Check `.env` file exists
- Verify API key is correct

**Error: "Permission denied"**
- Check token scopes include read/write
- Verify base access is granted

**Error: "Table not found"**
- Check table name matches exactly
- Verify base ID is correct

## Benefits

✅ **Centralized Storage** - All results in one place
✅ **Team Collaboration** - Share with team members
✅ **History Tracking** - See all past generations
✅ **Easy Export** - Export to CSV/Excel
✅ **Visual Gallery** - See thumbnails of all media
✅ **Filtering** - Filter by type, date, status
✅ **Analytics** - Track usage and performance
