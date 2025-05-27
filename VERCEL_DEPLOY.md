# Deploying to Vercel

## Prerequisites

1. Make sure you've exported your SQLite data to JSON by running:
   ```
   python export_data.py
   ```
   
2. Verify that the file exists at `static/data/earthquake_data.json`

3. Ensure your `vercel.json` file is properly configured

## Option 1: Deploy from the Vercel Dashboard

1. Push your code to a GitHub repository

2. Sign up/log in at [vercel.com](https://vercel.com)

3. Click "New Project" 

4. Import your repository from GitHub

5. Configure the project:
   - Framework preset: Other
   - Build command: (leave empty)
   - Output directory: (leave empty) 
   - Install command: pip install -r requirements.txt

6. Click "Deploy"

## Option 2: Deploy using the Vercel CLI

1. Install the Vercel CLI:
   ```
   npm i -g vercel
   ```

2. Login to Vercel:
   ```
   vercel login
   ```

3. Deploy by running the command in your project directory:
   ```
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy? Y
   - Which scope? (Select your account)
   - Link to existing project? N
   - Project name? (Choose or accept default)
   - Directory? ./
   - Override settings? N

5. For production deployment (when ready):
   ```
   vercel --prod
   ```

Once deployed, Vercel will provide a URL where your project is hosted.
