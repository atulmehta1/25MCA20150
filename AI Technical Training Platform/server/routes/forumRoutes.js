const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /api/forum
router.get('/', (req, res) => {
  const posts = db.getForumPosts();
  res.json({ success: true, count: posts.length, posts });
});

// POST /api/forum
router.post('/', (req, res) => {
  const { title, category, author, authorRole } = req.body;
  if (!title) {
    return res.status(400).json({ success: false, message: 'Question title is required.' });
  }

  const newPost = db.createForumPost({
    title,
    category: category || 'General',
    author: author || 'Student',
    authorRole: authorRole || 'Student'
  });

  res.status(201).json({ success: true, post: newPost });
});

// POST /api/forum/:id/reply
router.post('/:id/reply', (req, res) => {
  const { content, author, authorRole, isTrainerVerified } = req.body;
  if (!content) {
    return res.status(400).json({ success: false, message: 'Reply content is required.' });
  }

  const reply = db.addReplyToPost(req.params.id, {
    content,
    author: author || 'Anonymous',
    authorRole: authorRole || 'Student',
    isTrainerVerified: Boolean(isTrainerVerified)
  });

  if (!reply) {
    return res.status(404).json({ success: false, message: 'Post not found.' });
  }

  res.status(201).json({ success: true, reply });
});

// POST /api/forum/:id/upvote
router.post('/:id/upvote', (req, res) => {
  const posts = db.getForumPosts();
  const post = posts.find(p => p.id === req.params.id);
  if (post) {
    post.upvotes = (post.upvotes || 0) + 1;
    db.save();
    return res.json({ success: true, upvotes: post.upvotes });
  }
  res.status(404).json({ success: false, message: 'Post not found.' });
});

module.exports = router;
