import os
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import warnings

# 警告を抑制
warnings.filterwarnings("ignore")

# テスト用データパスを定義
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")

@pytest.fixture
def prepare_data():
    """Titanicデータセットを前処理して返す"""
    # データの読み込み
    df = pd.read_csv(DATA_PATH)
    
    # 欠損値の処理
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    
    # カテゴリ変数のエンコーディング
    df['Sex'] = df['Sex'].map({'female': 1, 'male': 0})
    embarked_dummies = pd.get_dummies(df['Embarked'], prefix='Embarked', drop_first=True)
    df = pd.concat([df, embarked_dummies], axis=1)
    
    # 使用する特徴量を選択
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked_Q', 'Embarked_S']
    X = df[features]
    y = df['Survived'].astype(int)
    
    return X, y

def test_feature_importance_balance(prepare_data):
    """特徴量の重要度が特定の特徴に過度に支配されていないことを検証"""
    X, y = prepare_data
    
    # ランダムフォレストモデルの学習
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 特徴量の重要度を取得
    feature_importances = model.feature_importances_
    
    # 重要度の最大値が全体の50%を超えていないことを確認
    max_importance = np.max(feature_importances)
    assert max_importance < 0.5, f"最も重要な特徴量が全体の50%以上({max_importance:.2%})を占めています。モデルが過度に1つの特徴に依存している可能性があります。"
    
    # 上位2つの特徴量の合計が全体の80%を超えていないことを確認
    top_two_sum = np.sum(np.sort(feature_importances)[-2:])
    assert top_two_sum < 0.8, f"上位2つの特徴量が全体の80%以上({top_two_sum:.2%})を占めています。モデルが少数の特徴に過度に依存している可能性があります。"
    
    # 全ての特徴量がある程度の重要度を持っていることを確認
    min_importance = np.min(feature_importances)
    assert min_importance > 0.01, f"最も重要度の低い特徴量の重要度が1%未満({min_importance:.2%})です。不要な特徴量がある可能性があります。"
    
    # 重要度のばらつきを確認（標準偏差が小さすぎないか）
    std_importance = np.std(feature_importances)
    assert 0.03 < std_importance < 0.2, f"特徴量の重要度の標準偏差が適切な範囲外({std_importance:.2%})です。"
    
    # コンソールに重要度を出力（デバッグ用）
    feature_importance_dict = dict(zip(X.columns, feature_importances))
    sorted_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)
    print("\n特徴量の重要度:")
    for feature, importance in sorted_importances:
        print(f"{feature}: {importance:.4f}")