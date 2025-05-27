# GitHub Pages Deployment Guide

This guide explains how to deploy your Earthquake Dashboard to GitHub Pages.

## Prerequisites
- A GitHub account
- Git installed on your computer

## Steps to Deploy

### 1. Create a GitHub Repository
- Go to [GitHub](https://github.com) and sign in
- Click the "+" icon in the top right and select "New repository"
- Name your repository `earthquake_project`
- Make it public
- Initialize with a README if prompted
- Click "Create repository"

### 2. Push Your Code to GitHub
```bash
# In your project directory
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/earthquake_project.git
git push -u origin main
```

### 3. Configure GitHub Pages
- Go to your repository on GitHub
- Click on "Settings"
- Scroll down to "GitHub Pages" section
- Under "Source", select "main" branch
- Click "Save"
- Wait a few minutes for your site to deploy

### 4. Access Your Live Site
- Your site will be available at: `https://YOUR_GITHUB_USERNAME.github.io/earthquake_project/`

## Static Dataset Preparation

Since GitHub Pages can only serve static files and doesn't support backend servers, we've included:

1. A pre-populated dataset in the static folder
2. A simplified version of the app that loads data directly from JSON files

## Making Updates

To update your site after making changes:
```bash
git add .
git commit -m "Your update description"
git push origin main
```

Your changes will automatically deploy to GitHub Pages (may take a few minutes).
