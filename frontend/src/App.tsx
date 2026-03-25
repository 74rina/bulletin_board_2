import { useEffect, useMemo, useState } from 'react'
import './App.css'

type PostListItem = {
  id: number
  name: string
  title: string
  body: string
  created_at: string
  comment_count: number
}

type Comment = {
  id: number
  body: string
  created_at: string
}

type PostDetail = {
  id: number
  name: string
  title: string
  body: string
  created_at: string
  comments: Comment[]
}

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8002'

const formatDate = (value: string) => {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return new Intl.DateTimeFormat('ja-JP', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function App() {
  const [posts, setPosts] = useState<PostListItem[]>([])
  const [selectedPostId, setSelectedPostId] = useState<number | null>(null)
  const [selectedPost, setSelectedPost] = useState<PostDetail | null>(null)
  const [loadingPosts, setLoadingPosts] = useState(false)
  const [loadingPostDetail, setLoadingPostDetail] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [name, setName] = useState('')
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [commentBody, setCommentBody] = useState('')

  const selectedPostMeta = useMemo(() => {
    if (!selectedPostId) return null
    return posts.find((post) => post.id === selectedPostId) ?? null
  }, [posts, selectedPostId])

  const fetchPosts = async () => {
    setLoadingPosts(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/posts`)
      if (!res.ok) throw new Error('投稿一覧の取得に失敗しました。')
      const data = (await res.json()) as PostListItem[]
      setPosts(data)
      if (data.length && !selectedPostId) {
        setSelectedPostId(data[0].id)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'エラーが発生しました。')
    } finally {
      setLoadingPosts(false)
    }
  }

  const fetchPostDetail = async (postId: number) => {
    setLoadingPostDetail(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/posts/${postId}`)
      if (!res.ok) throw new Error('投稿詳細の取得に失敗しました。')
      const data = (await res.json()) as PostDetail
      setSelectedPost(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'エラーが発生しました。')
    } finally {
      setLoadingPostDetail(false)
    }
  }

  useEffect(() => {
    fetchPosts()
  }, [])

  useEffect(() => {
    if (selectedPostId) {
      fetchPostDetail(selectedPostId)
    } else {
      setSelectedPost(null)
    }
  }, [selectedPostId])

  const handleCreatePost = async (event: React.FormEvent) => {
    event.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, title, body }),
      })
      if (!res.ok) throw new Error('投稿の作成に失敗しました。')
      setName('')
      setTitle('')
      setBody('')
      await fetchPosts()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'エラーが発生しました。')
    }
  }

  const handleCreateComment = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!selectedPostId) return
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/posts/${selectedPostId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ body: commentBody }),
      })
      if (!res.ok) throw new Error('コメントの投稿に失敗しました。')
      setCommentBody('')
      await fetchPosts()
      await fetchPostDetail(selectedPostId)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'エラーが発生しました。')
    }
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <p className="eyebrow">匿名掲示板</p>
          <h1>話したいことを、気軽に投稿しよう。</h1>
          <p className="lead">
            だれでも匿名で投稿・コメントできる、ライトなコミュニティ空間。
          </p>
        </div>
        <div className="hero-panel">
          <form className="card" onSubmit={handleCreatePost}>
            <h2>新規投稿</h2>
            <label>
              名前
              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="例: 匿名さん"
                required
              />
            </label>
            <label>
              タイトル
              <input
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="気になっていること"
                required
              />
            </label>
            <label>
              本文
              <textarea
                value={body}
                onChange={(event) => setBody(event.target.value)}
                placeholder="内容を自由に書いてください"
                required
              />
            </label>
            <button type="submit">投稿する</button>
          </form>
        </div>
      </header>

      <main className="layout">
        <section className="panel">
          <div className="panel-header">
            <h2>投稿一覧</h2>
            <span className="meta">
              {loadingPosts ? '読み込み中...' : `${posts.length} 件`}
            </span>
          </div>
          {error && <p className="error">{error}</p>}
          <div className="post-list">
            {posts.map((post) => (
              <button
                key={post.id}
                className={`post-card ${
                  selectedPostId === post.id ? 'active' : ''
                }`}
                onClick={() => setSelectedPostId(post.id)}
              >
                <div>
                  <h3>{post.title}</h3>
                  <p className="excerpt">{post.body}</p>
                </div>
                <div className="post-meta">
                  <span>{formatDate(post.created_at)}</span>
                  <span className="pill">コメント {post.comment_count}</span>
                </div>
              </button>
            ))}
            {!posts.length && !loadingPosts && (
              <p className="empty">まだ投稿がありません。</p>
            )}
          </div>
        </section>

        <section className="panel detail">
          <div className="panel-header">
            <h2>投稿詳細</h2>
            {selectedPostMeta && (
              <span className="meta">{selectedPostMeta.name}</span>
            )}
          </div>
          {loadingPostDetail && <p className="empty">読み込み中...</p>}
          {!loadingPostDetail && selectedPost && (
            <div className="detail-content">
              <div className="detail-header">
                <h3>{selectedPost.title}</h3>
                <p className="detail-body">{selectedPost.body}</p>
                <div className="detail-meta">
                  <span>{formatDate(selectedPost.created_at)}</span>
                  <span className="pill">
                    コメント {selectedPost.comments.length}
                  </span>
                </div>
              </div>

              <div className="comments">
                <h4>コメント</h4>
                <div className="comment-list">
                  {selectedPost.comments.map((comment) => (
                    <div key={comment.id} className="comment">
                      <p>{comment.body}</p>
                      <span>{formatDate(comment.created_at)}</span>
                    </div>
                  ))}
                  {!selectedPost.comments.length && (
                    <p className="empty">まだコメントがありません。</p>
                  )}
                </div>
              </div>

              <form className="card comment-form" onSubmit={handleCreateComment}>
                <h4>コメントを書く</h4>
                <label>
                  本文
                  <textarea
                    value={commentBody}
                    onChange={(event) => setCommentBody(event.target.value)}
                    placeholder="コメントを入力してください"
                    required
                  />
                </label>
                <button type="submit">コメントする</button>
              </form>
            </div>
          )}
          {!loadingPostDetail && !selectedPost && (
            <p className="empty">投稿を選択してください。</p>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
