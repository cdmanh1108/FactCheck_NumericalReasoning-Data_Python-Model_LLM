import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")

# ===== TẢI DỮ LIỆU =====
# Dùng Path(__file__) để tính đường dẫn tuyệt đối - không bị lỗi dù chạy từ đâu
project_root = Path(__file__).parent.parent
file_path = project_root / "data" / "members" / "generated_vinumfcr_200_samples.xlsx"

df = pd.read_excel(file_path)
df['Evidence_Length'] = df['Evidence'].apply(lambda x: len(str(x).split()))
df['Statement_Length'] = df['Statement'].apply(lambda x: len(str(x).split()))

print(f"Tổng số mẫu: {len(df)}")

# ===== VẼ 4 BIỂU ĐỒ =====
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle('BÁO CÁO PHÂN TÍCH DỮ LIỆU (EDA) - VINUMFCR', fontsize=18, fontweight='bold')

# Biểu đồ 1: Phân bổ nhãn
label_names = {0: '0: Hỗ trợ', 1: '1: Bác bỏ', 2: '2: Thiếu TT'}
counts = df['labels'].map(label_names).value_counts()
bars = axes[0,0].bar(counts.index, counts.values, color=['#2ecc71','#e74c3c','#f39c12'])
for bar in bars:
    axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   str(int(bar.get_height())), ha='center', fontweight='bold')
axes[0,0].set_title('PHÂN BỔ NHÃN (Label Distribution)', fontweight='bold')
axes[0,0].set_ylabel('Số lượng câu')

# Biểu đồ 2: Độ dài bài báo (Evidence)
axes[0,1].hist(df['Evidence_Length'], bins=25, color='steelblue', edgecolor='white')
axes[0,1].axvline(df['Evidence_Length'].mean(), color='red', linestyle='--', label=f"TB: {df['Evidence_Length'].mean():.0f} từ")
axes[0,1].set_title('ĐỘ DÀI BÀI BÁO (Evidence)', fontweight='bold')
axes[0,1].set_xlabel('Số từ')
axes[0,1].legend()

# Biểu đồ 3: Loại lập luận (Reasoning Type)
if 'Reasoning_Type' in df.columns:
    rc = df['Reasoning_Type'].value_counts()
    axes[1,0].barh(rc.index, rc.values, color='mediumpurple')
    axes[1,0].set_title('PHÂN BỔ LOẠI LẬP LUẬN', fontweight='bold')
    axes[1,0].set_xlabel('Số lượng')

# Biểu đồ 4: Loại bằng chứng (Evidence Type)
if 'Evidence_Type' in df.columns:
    ec = df['Evidence_Type'].value_counts()
    axes[1,1].pie(ec.values, labels=ec.index, autopct='%1.1f%%', startangle=90,
                  colors=['#3498db','#e67e22','#2ecc71'])
    axes[1,1].set_title('LOẠI BẰNG CHỨNG (Evidence Type)', fontweight='bold')

plt.tight_layout()
plt.savefig('eda_report.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Đã vẽ xong 4 biểu đồ!")
print(f"Bài báo dài nhất: {df['Evidence_Length'].max()} từ")
print(f"Bài báo trung bình: {df['Evidence_Length'].mean():.0f} từ")
print(f"Câu tuyên bố trung bình: {df['Statement_Length'].mean():.0f} từ")
