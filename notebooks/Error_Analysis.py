import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

# ===== TẢI DỮ LIỆU =====
project_root = Path(__file__).parent.parent
results_path = project_root / "data" / "processed" / "finetuned_results.csv"

if not results_path.exists():
    raise FileNotFoundError(
        f"Chưa có file kết quả dự đoán!\n"
        f"Hãy chạy Inference trên Google Colab trước, "
        f"sau đó tải file finetuned_results.csv về đặt tại:\n{results_path}"
    )

df_test = pd.read_csv(results_path)

# Lọc ra các câu AI đoán SAI
error_df = df_test[df_test['labels'] != df_test['Predicted_Label']].copy()

print(f"✅ Tổng số câu test     : {len(df_test)}")
print(f"✅ Số câu AI đoán ĐÚNG  : {len(df_test) - len(error_df)}")
print(f"❌ Số câu AI đoán SAI   : {len(error_df)}  ({len(error_df)/len(df_test)*100:.1f}%)")
print("=" * 50)

# ===== XUẤT FILE ERROR ANALYSIS =====
cols = ['labels', 'Predicted_Label', 'Statement', 'Evidence']
error_df = error_df[cols + [c for c in error_df.columns if c not in cols]]

error_path = project_root / "data" / "processed" / "error_analysis.csv"
error_df.to_csv(error_path, index=False, encoding='utf-8-sig')
print(f"💾 Đã lưu file Error Analysis tại: {error_path}")
print("=" * 50)

# ===== VẼ BIỂU ĐỒ PHÂN TÍCH LỖI =====
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('PHÂN TÍCH LỖI CỦA MÔ HÌNH AI (ERROR ANALYSIS)', fontsize=15, fontweight='bold')

# Biểu đồ 1: AI hay sai ở Dạng Toán nào nhất?
if 'Reasoning_Type' in error_df.columns:
    rc = error_df['Reasoning_Type'].value_counts()
    axes[0].barh(rc.index, rc.values, color='tomato')
    axes[0].set_title('AI HAY SAI Ở DẠNG TOÁN NÀO NHẤT?', fontweight='bold')
    axes[0].set_xlabel('Số câu sai')
    axes[0].set_ylabel('Dạng Toán (Reasoning Type)')
    for i, v in enumerate(rc.values):
        axes[0].text(v + 0.1, i, str(v), va='center', fontweight='bold')

# Biểu đồ 2: AI hay đoán nhầm vào nhãn nào?
pred_counts = error_df['Predicted_Label'].value_counts().sort_index()
label_map = {0: '0 (Support)', 1: '1 (Refute)', 2: '2 (NEI)'}
axes[1].bar(pred_counts.index.map(label_map), pred_counts.values, color='darkorange')
axes[1].set_title('AI HAY BỊ ẢO GIÁC ĐOÁN VÀO NHÃN NÀO?', fontweight='bold')
axes[1].set_xlabel('Nhãn AI dự đoán sai')
axes[1].set_ylabel('Số lượng câu')
for i, v in enumerate(pred_counts.values):
    axes[1].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(project_root / "notebooks" / "error_analysis.png", dpi=150)
plt.show()
print("💾 Đã lưu biểu đồ tại: notebooks/error_analysis.png")
