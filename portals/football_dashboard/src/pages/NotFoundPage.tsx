import React from 'react'
import Layout from '../components/Layout'
import styles from "./NotFoundPage.module.css"

const NotFoundPage: React.FC = () => {
  return (
    <Layout>
        <h1 className={styles.heading}>NotFoundPage</h1>
    </Layout>
  )
}

export default NotFoundPage